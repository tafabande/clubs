"""
Church ViewSet and related views.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count

from apps.permissions.permissions import IsOrganizationAdmin
from ..models import Church, ChurchMembership
from ..serializers import ChurchSerializer, ChurchCreateSerializer, ChurchMembershipSerializer


class ChurchViewSet(viewsets.ModelViewSet):
    """ViewSet for Church model."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Church.objects.annotate(member_count=Count('memberships'))
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ChurchCreateSerializer
        return ChurchSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOrganizationAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a church."""
        church = self.get_object()
        
        existing = ChurchMembership.objects.filter(user=request.user, church=church).first()
        if existing:
            return Response({'error': f'Already a member (status: {existing.status})'}, status=400)
        
        membership = ChurchMembership.objects.create(user=request.user, church=church, status='active')
        return Response(ChurchMembershipSerializer(membership).data, status=201)
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a church."""
        church = self.get_object()
        membership = ChurchMembership.objects.filter(user=request.user, church=church).first()
        
        if not membership:
            return Response({'error': 'Not a member'}, status=400)
        
        membership.status = 'inactive'
        membership.save()
        return Response({'message': 'Left successfully'})
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """List church members."""
        church = self.get_object()
        memberships = ChurchMembership.objects.filter(church=church, status='active')
        return Response(ChurchMembershipSerializer(memberships, many=True).data)
