"""
Serializers for organization models.
"""
from rest_framework import serializers
from django.db.models import Count
from apps.users.serializers import UserSerializer
from ..models import (
    Club, ClubMembership,
    Church, ChurchMembership,
    SportsTeam, SportsTeamMembership,
    Activity, ActivityRegistration,
    OrganizationHistory
)


# Club Serializers
class ClubMembershipSerializer(serializers.ModelSerializer):
    """Serializer for club membership."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ClubMembership
        fields = ['id', 'user', 'club', 'status', 'position', 'joined_at', 'approved_by', 'approved_at']
        read_only_fields = ['id', 'joined_at', 'approved_by', 'approved_at']


class ClubSerializer(serializers.ModelSerializer):
    """Serializer for Club model."""
    created_by = UserSerializer(read_only=True)
    faculty_advisor = UserSerializer(read_only=True)
    user_membership = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    organization_type = serializers.SerializerMethodField()
    contact_email = serializers.ReadOnlyField(source='email')
    
    class Meta:
        model = Club
        fields = [
            'id', 'name', 'description', 'email', 'contact_email', 'contact_phone', 'website', 'logo', 'cover_photo',
            'category', 'categories', 'faculty_advisor', 'meeting_location', 'meeting_schedule',
            'max_members', 'is_active', 'is_approved', 'approved_by', 'approved_at',
            'created_by', 'created_at', 'updated_at', 
            'members_count', 'followers_count', 'posts_count', 'events_count',
            'user_membership', 'is_member', 'organization_type'
        ]
        read_only_fields = ['id', 'is_approved', 'approved_by', 'approved_at', 'created_by', 'created_at', 'updated_at']
    
    def get_user_membership(self, obj):
        """Get current user's membership status."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            membership = ClubMembership.objects.filter(user=request.user, club=obj).first()
            if membership:
                return ClubMembershipSerializer(membership).data
        return None

    def get_is_member(self, obj):
        """Check if current user is a member."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ClubMembership.objects.filter(user=request.user, club=obj, status='active').exists()
        return False

    def get_organization_type(self, obj):
        return 'club'


class ClubCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating clubs."""
    
    class Meta:
        model = Club
        fields = [
            'name', 'description', 'email', 'website', 'logo',
            'category', 'meeting_location', 'meeting_schedule', 'max_members'
        ]
    
    def create(self, validated_data):
        """Create club with current user as creator."""
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)


# Church Serializers
class ChurchMembershipSerializer(serializers.ModelSerializer):
    """Serializer for church membership."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ChurchMembership
        fields = ['id', 'user', 'church', 'status', 'ministry', 'joined_at']
        read_only_fields = ['id', 'joined_at']


class ChurchSerializer(serializers.ModelSerializer):
    """Serializer for Church model."""
    created_by = UserSerializer(read_only=True)
    user_membership = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    organization_type = serializers.SerializerMethodField()
    contact_email = serializers.ReadOnlyField(source='email')
    
    class Meta:
        model = Church
        fields = [
            'id', 'name', 'description', 'email', 'contact_email', 'contact_phone', 'website', 'logo', 'cover_photo',
            'denomination', 'categories', 'service_times', 'pastor_name', 'pastor_contact',
            'is_active', 'is_approved', 'approved_by', 'approved_at',
            'created_by', 'created_at', 'updated_at', 
            'members_count', 'followers_count', 'posts_count', 'events_count',
            'user_membership', 'is_member', 'organization_type'
        ]
        read_only_fields = ['id', 'is_approved', 'approved_by', 'approved_at', 'created_by', 'created_at', 'updated_at']
    
    def get_user_membership(self, obj):
        """Get current user's membership status."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            membership = ChurchMembership.objects.filter(user=request.user, church=obj).first()
            if membership:
                return ChurchMembershipSerializer(membership).data
        return None

    def get_is_member(self, obj):
        """Check if current user is a member."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ChurchMembership.objects.filter(user=request.user, church=obj, status='active').exists()
        return False

    def get_organization_type(self, obj):
        return 'church'


class ChurchCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating churches."""
    
    class Meta:
        model = Church
        fields = [
            'name', 'description', 'email', 'website', 'logo',
            'denomination', 'service_times', 'pastor_name', 'pastor_contact'
        ]
    
    def create(self, validated_data):
        """Create church with current user as creator."""
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)


# Sports Team Serializers
class SportsTeamMembershipSerializer(serializers.ModelSerializer):
    """Serializer for sports team membership."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = SportsTeamMembership
        fields = ['id', 'user', 'sports_team', 'position', 'jersey_number', 'status', 'joined_at']
        read_only_fields = ['id', 'joined_at']


class SportsTeamSerializer(serializers.ModelSerializer):
    """Serializer for SportsTeam model."""
    created_by = UserSerializer(read_only=True)
    user_membership = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    organization_type = serializers.SerializerMethodField()
    contact_email = serializers.ReadOnlyField(source='email')
    
    class Meta:
        model = SportsTeam
        fields = [
            'id', 'name', 'description', 'email', 'contact_email', 'contact_phone', 'website', 'logo', 'cover_photo',
            'sport_type', 'categories', 'division', 'coach', 'practice_schedule', 'max_roster_size',
            'is_active', 'is_approved', 'approved_by', 'approved_at',
            'created_by', 'created_at', 'updated_at', 
            'members_count', 'followers_count', 'posts_count', 'events_count',
            'user_membership', 'is_member', 'organization_type'
        ]
        read_only_fields = ['id', 'is_approved', 'approved_by', 'approved_at', 'created_by', 'created_at', 'updated_at']
    
    def get_user_membership(self, obj):
        """Get current user's membership status."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            membership = SportsTeamMembership.objects.filter(user=request.user, sports_team=obj).first()
            if membership:
                return SportsTeamMembershipSerializer(membership).data
        return None

    def get_is_member(self, obj):
        """Check if current user is a member."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SportsTeamMembership.objects.filter(user=request.user, sports_team=obj, status='active').exists()
        return False

    def get_organization_type(self, obj):
        return 'sports_team'


class SportsTeamCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating sports teams."""
    
    class Meta:
        model = SportsTeam
        fields = [
            'name', 'description', 'email', 'website', 'logo',
            'sport_type', 'division', 'coach', 'practice_schedule', 'max_roster_size'
        ]
    
    def create(self, validated_data):
        """Create sports team with current user as creator."""
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)


# Activity Serializers
class ActivityRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for activity registration."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ActivityRegistration
        fields = ['id', 'user', 'activity', 'status', 'registration_data', 'registered_at']
        read_only_fields = ['id', 'registered_at']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model."""
    created_by = UserSerializer(read_only=True)
    user_registration = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    organization_type = serializers.SerializerMethodField()
    contact_email = serializers.ReadOnlyField(source='email')
    
    class Meta:
        model = Activity
        fields = [
            'id', 'name', 'description', 'email', 'contact_email', 'contact_phone', 'website', 'logo', 'cover_photo',
            'activity_type', 'categories', 'start_date', 'end_date', 'location',
            'max_participants', 'registration_deadline', 'is_recurring',
            'is_active', 'is_approved', 'approved_by', 'approved_at',
            'created_by', 'created_at', 'updated_at', 
            'members_count', 'followers_count', 'posts_count', 'events_count',
            'user_registration', 'is_member', 'organization_type'
        ]
        read_only_fields = ['id', 'is_approved', 'approved_by', 'approved_at', 'created_by', 'created_at', 'updated_at']
    
    def get_user_registration(self, obj):
        """Get current user's registration status."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            registration = ActivityRegistration.objects.filter(user=request.user, activity=obj).first()
            if registration:
                return ActivityRegistrationSerializer(registration).data
        return None

    def get_is_member(self, obj):
        """Check if current user is registered for the activity."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ActivityRegistration.objects.filter(user=request.user, activity=obj, status='registered').exists()
        return False

    def get_organization_type(self, obj):
        return 'activity'


class ActivityCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating activities."""
    
    class Meta:
        model = Activity
        fields = [
            'name', 'description', 'email', 'website', 'logo',
            'activity_type', 'start_date', 'end_date', 'location',
            'max_participants', 'registration_deadline', 'is_recurring'
        ]
    
    def create(self, validated_data):
        """Create activity with current user as creator."""
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)


# Organization History Serializer
class OrganizationHistorySerializer(serializers.ModelSerializer):
    """Serializer for organization history."""
    
    class Meta:
        model = OrganizationHistory
        fields = ['id', 'date', 'member_count', 'event_count', 'engagement_score']
        read_only_fields = ['id']
