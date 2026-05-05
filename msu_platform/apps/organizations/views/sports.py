"""
Sports Team ViewSet and related views.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count

from apps.permissions.permissions import IsOrganizationAdmin
from ..models import SportsTeam, SportsTeamMembership
from ..serializers import SportsTeamSerializer, SportsTeamCreateSerializer, SportsTeamMembershipSerializer


class SportsTeamViewSet(viewsets.ModelViewSet):
    """ViewSet for SportsTeam model."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = SportsTeam.objects.annotate(member_count=Count('memberships'))
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SportsTeamCreateSerializer
        return SportsTeamSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOrganizationAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a sports team."""
        team = self.get_object()
        
        existing = SportsTeamMembership.objects.filter(user=request.user, sports_team=team).first()
        if existing:
            return Response({'error': f'Already a member (status: {existing.status})'}, status=400)
        
        # Check roster capacity
        current_members = SportsTeamMembership.objects.filter(sports_team=team, status='active').count()
        if current_members >= team.max_roster_size:
            return Response({'error': 'Team is at maximum capacity'}, status=400)
        
        membership = SportsTeamMembership.objects.create(
            user=request.user,
            sports_team=team,
            status='active'
        )
        return Response(SportsTeamMembershipSerializer(membership).data, status=201)
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a sports team."""
        team = self.get_object()
        membership = SportsTeamMembership.objects.filter(user=request.user, sports_team=team).first()
        
        if not membership:
            return Response({'error': 'Not a member'}, status=400)
        
        membership.status = 'inactive'
        membership.save()
        return Response({'message': 'Left team successfully'})
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """List team members (roster)."""
        team = self.get_object()
        memberships = SportsTeamMembership.objects.filter(sports_team=team, status='active')
        return Response(SportsTeamMembershipSerializer(memberships, many=True).data)
