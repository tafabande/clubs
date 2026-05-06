"""
Activity ViewSet and related views.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count
from django.utils import timezone

from apps.permissions.permissions import IsOrganizationAdmin
from ..models import Activity, ActivityRegistration
from ..serializers import ActivitySerializer, ActivityCreateSerializer, ActivityRegistrationSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity model."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Activity.objects.annotate(participant_count=Count('registrations'))
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)
        return queryset.order_by('-start_date')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ActivityCreateSerializer
        return ActivitySerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOrganizationAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        """Register for an activity."""
        activity = self.get_object()
        
        # Check if already registered
        existing = ActivityRegistration.objects.filter(user=request.user, activity=activity).first()
        if existing:
            return Response({'error': f'Already registered (status: {existing.status})'}, status=400)
        
        # Check if registration deadline passed
        if activity.registration_deadline < timezone.now():
            return Response({'error': 'Registration deadline has passed'}, status=400)
        
        # Check capacity
        current_participants = ActivityRegistration.objects.filter(activity=activity, status='registered').count()
        if current_participants >= activity.max_participants:
            return Response({'error': 'Activity is at maximum capacity'}, status=400)
        
        registration_data = request.data.get('registration_data', {})
        registration = ActivityRegistration.objects.create(
            user=request.user,
            activity=activity,
            status='registered',
            registration_data=registration_data
        )
        return Response(ActivityRegistrationSerializer(registration).data, status=201)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel activity registration."""
        activity = self.get_object()
        registration = ActivityRegistration.objects.filter(user=request.user, activity=activity).first()
        
        if not registration:
            return Response({'error': 'Not registered'}, status=400)
        
        registration.status = 'cancelled'
        registration.save()
        return Response({'message': 'Registration cancelled successfully'})
    
    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        """List activity participants."""
        activity = self.get_object()
        registrations = ActivityRegistration.objects.filter(activity=activity, status='registered')
        return Response(ActivityRegistrationSerializer(registrations, many=True).data)
