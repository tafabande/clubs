"""
Club ViewSet and related views.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count
from django.utils import timezone

from apps.permissions.permissions import HasPermission, IsOrganizationAdmin
from apps.permissions.services import PermissionService
from ..models import Club, ClubMembership, OrganizationHistory
from ..serializers import (
    ClubSerializer,
    ClubCreateSerializer,
    ClubMembershipSerializer,
    OrganizationHistorySerializer
)


class ClubViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Club model.
    
    Provides CRUD operations and custom actions for club management.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get clubs based on user permissions."""
        queryset = Club.objects.annotate(member_count=Count('memberships'))
        
        # Show all approved clubs to authenticated users
        # Show unapproved clubs only to creators and admins
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'create':
            return ClubCreateSerializer
        return ClubSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOrganizationAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Create club with current user as creator."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a club."""
        club = self.get_object()
        
        # Check if already a member
        existing = ClubMembership.objects.filter(user=request.user, club=club).first()
        if existing:
            return Response(
                {'error': f'You are already a member with status: {existing.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if club is at capacity
        current_members = ClubMembership.objects.filter(club=club, status='active').count()
        if current_members >= club.max_members:
            return Response(
                {'error': 'Club is at maximum capacity'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create membership request
        membership = ClubMembership.objects.create(
            user=request.user,
            club=club,
            status='pending'
        )
        
        return Response(
            ClubMembershipSerializer(membership).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a club."""
        club = self.get_object()
        
        membership = ClubMembership.objects.filter(user=request.user, club=club).first()
        if not membership:
            return Response(
                {'error': 'You are not a member of this club'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update status to inactive instead of deleting
        membership.status = 'inactive'
        membership.save()
        
        return Response(
            {'message': 'Successfully left the club'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """List club members."""
        club = self.get_object()
        
        # Check permission
        has_perm = PermissionService.check_user_permission(
            request.user, 'can_view_club_analytics', club
        )
        if not has_perm and not request.user.is_staff:
            # Only show active members to non-admins
            memberships = ClubMembership.objects.filter(club=club, status='active')
        else:
            # Show all memberships to admins
            memberships = ClubMembership.objects.filter(club=club)
        
        serializer = ClubMembershipSerializer(memberships, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOrganizationAdmin])
    def approve_member(self, request, pk=None):
        """Approve a pending member."""
        club = self.get_object()
        membership_id = request.data.get('membership_id')
        
        if not membership_id:
            return Response(
                {'error': 'membership_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            membership = ClubMembership.objects.get(id=membership_id, club=club)
        except ClubMembership.DoesNotExist:
            return Response(
                {'error': 'Membership not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if membership.status != 'pending':
            return Response(
                {'error': f'Membership is not pending (current status: {membership.status})'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        membership.status = 'active'
        membership.approved_by = request.user
        membership.approved_at = timezone.now()
        membership.save()
        
        return Response(ClubMembershipSerializer(membership).data)
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get club analytics history."""
        club = self.get_object()
        
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(Club)
        
        history = OrganizationHistory.objects.filter(
            content_type=content_type,
            object_id=club.id
        ).order_by('-date')[:30]  # Last 30 days
        
        serializer = OrganizationHistorySerializer(history, many=True)
        return Response(serializer.data)
