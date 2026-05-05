"""
Serializers for search functionality.
"""
from rest_framework import serializers
from apps.organizations.models import SearchIndex, PopularSearch


class SearchIndexSerializer(serializers.ModelSerializer):
    """Serializer for search index entries."""

    class Meta:
        model = SearchIndex
        fields = [
            'id', 'organization_type', 'organization_id', 'name',
            'description', 'category', 'tags', 'is_active',
            'is_approved', 'member_count', 'created_at', 'updated_at'
        ]
        read_only_fields = fields


class PopularSearchSerializer(serializers.ModelSerializer):
    """Serializer for popular/trending searches."""

    class Meta:
        model = PopularSearch
        fields = ['id', 'query', 'search_count', 'last_searched', 'created_at']
        read_only_fields = fields


class SearchResultSerializer(serializers.Serializer):
    """Serializer for enriched search results."""

    id = serializers.UUIDField()
    type = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    category = serializers.CharField()
    member_count = serializers.IntegerField()
    is_approved = serializers.BooleanField()
    organization = serializers.SerializerMethodField()

    def get_organization(self, obj):
        """Get organization details based on type."""
        from apps.organizations.serializers import (
            ClubSerializer, ChurchSerializer,
            SportsTeamSerializer, ActivitySerializer
        )

        org = obj.get('organization')
        if not org:
            return None

        org_type = obj.get('type')

        if org_type == 'club':
            return ClubSerializer(org, context=self.context).data
        elif org_type == 'church':
            return ChurchSerializer(org, context=self.context).data
        elif org_type == 'sports_team':
            return SportsTeamSerializer(org, context=self.context).data
        elif org_type == 'activity':
            return ActivitySerializer(org, context=self.context).data

        return None
