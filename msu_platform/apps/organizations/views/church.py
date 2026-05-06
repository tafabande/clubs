"""
Church ViewSet and related views.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from apps.permissions.permissions import IsOrganizationAdmin
from ..models import Church, ChurchMembership, Post
from ..serializers import (
    ChurchSerializer,
    ChurchCreateSerializer,
    ChurchMembershipSerializer,
    PostSerializer
)


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
    def posts(self, request, pk=None):
        """Get church posts."""
        church = self.get_object()
        content_type = ContentType.objects.get_for_model(Church)
        posts = Post.objects.filter(
            content_type=content_type,
            object_id=church.id,
            is_active=True
        ).order_by('-is_pinned', '-created_at')

        if not request.user.is_staff:
            posts = posts.filter(
                models.Q(visibility='public') |
                models.Q(author=request.user)
            )

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """List church members."""
        church = self.get_object()
        memberships = ChurchMembership.objects.filter(church=church, status='active')
        return Response(ChurchMembershipSerializer(memberships, many=True).data)
