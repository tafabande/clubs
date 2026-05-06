"""
Admin configuration for organizations app.
"""
from django.contrib import admin
from .models import (
    Club, ClubMembership,
    Church, ChurchMembership,
    SportsTeam, SportsTeamMembership,
    Activity, ActivityRegistration,
    OrganizationHistory,
    Post, PostMedia, PostLike, PostComment, PostShare, Feed,
    SearchIndex, PopularSearch
)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Admin for Club model."""
    list_display = ['name', 'category', 'is_active', 'is_approved', 'created_by', 'created_at']
    list_filter = ['is_active', 'is_approved', 'category', 'created_at']
    search_fields = ['name', 'description', 'email']
    readonly_fields = ['created_at', 'updated_at', 'approved_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'email', 'website', 'logo', 'category')
        }),
        ('Club Details', {
            'fields': ('faculty_advisor', 'meeting_location', 'meeting_schedule', 'max_members')
        }),
        ('Status', {
            'fields': ('is_active', 'is_approved', 'approved_by', 'approved_at')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(ClubMembership)
class ClubMembershipAdmin(admin.ModelAdmin):
    """Admin for ClubMembership model."""
    list_display = ['user', 'club', 'status', 'position', 'joined_at']
    list_filter = ['status', 'joined_at']
    search_fields = ['user__email', 'club__name']
    readonly_fields = ['joined_at', 'approved_at']


@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    """Admin for Church model."""
    list_display = ['name', 'denomination', 'is_active', 'is_approved', 'created_by', 'created_at']
    list_filter = ['is_active', 'is_approved', 'denomination', 'created_at']
    search_fields = ['name', 'description', 'email']
    readonly_fields = ['created_at', 'updated_at', 'approved_at']


@admin.register(ChurchMembership)
class ChurchMembershipAdmin(admin.ModelAdmin):
    """Admin for ChurchMembership model."""
    list_display = ['user', 'church', 'status', 'ministry', 'joined_at']
    list_filter = ['status', 'joined_at']
    search_fields = ['user__email', 'church__name']


@admin.register(SportsTeam)
class SportsTeamAdmin(admin.ModelAdmin):
    """Admin for SportsTeam model."""
    list_display = ['name', 'sport_type', 'division', 'is_active', 'is_approved', 'created_by', 'created_at']
    list_filter = ['is_active', 'is_approved', 'sport_type', 'division', 'created_at']
    search_fields = ['name', 'description', 'email']
    readonly_fields = ['created_at', 'updated_at', 'approved_at']


@admin.register(SportsTeamMembership)
class SportsTeamMembershipAdmin(admin.ModelAdmin):
    """Admin for SportsTeamMembership model."""
    list_display = ['user', 'sports_team', 'position', 'jersey_number', 'status', 'joined_at']
    list_filter = ['status', 'joined_at']
    search_fields = ['user__email', 'sports_team__name']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin for Activity model."""
    list_display = ['name', 'activity_type', 'start_date', 'end_date', 'is_active', 'is_approved', 'created_by']
    list_filter = ['is_active', 'is_approved', 'activity_type', 'start_date', 'is_recurring']
    search_fields = ['name', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at', 'approved_at']


@admin.register(ActivityRegistration)
class ActivityRegistrationAdmin(admin.ModelAdmin):
    """Admin for ActivityRegistration model."""
    list_display = ['user', 'activity', 'status', 'registered_at']
    list_filter = ['status', 'registered_at']
    search_fields = ['user__email', 'activity__name']


@admin.register(OrganizationHistory)
class OrganizationHistoryAdmin(admin.ModelAdmin):
    """Admin for OrganizationHistory model."""
    list_display = ['content_type', 'object_id', 'date', 'member_count', 'event_count', 'engagement_score']
    list_filter = ['date', 'content_type']
    readonly_fields = ['date']


# Feed and Social Media Models

class PostMediaInline(admin.TabularInline):
    """Inline admin for post media."""
    model = PostMedia
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin for Post model."""
    list_display = ['title', 'author', 'post_type', 'visibility', 'is_pinned', 'likes_count', 'comments_count', 'created_at']
    list_filter = ['post_type', 'visibility', 'is_pinned', 'is_active', 'created_at']
    search_fields = ['title', 'content', 'author__email']
    readonly_fields = ['likes_count', 'comments_count', 'shares_count', 'created_at', 'updated_at']
    inlines = [PostMediaInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('author', 'content_type', 'object_id', 'post_type', 'title', 'content')
        }),
        ('Media', {
            'fields': ('image', 'video')
        }),
        ('Event Details', {
            'fields': ('event_date', 'event_location', 'event_link'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('visibility', 'is_pinned', 'tags', 'is_active')
        }),
        ('Engagement', {
            'fields': ('likes_count', 'comments_count', 'shares_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    """Admin for PostMedia model."""
    list_display = ['post', 'media_type', 'order', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['post__title', 'caption']
    readonly_fields = ['created_at']


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    """Admin for PostLike model."""
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'post__title']
    readonly_fields = ['created_at']


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    """Admin for PostComment model."""
    list_display = ['user', 'post', 'parent', 'likes_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__email', 'post__title', 'content']
    readonly_fields = ['likes_count', 'created_at', 'updated_at']


@admin.register(PostShare)
class PostShareAdmin(admin.ModelAdmin):
    """Admin for PostShare model."""
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'post__title', 'comment']
    readonly_fields = ['created_at']


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    """Admin for Feed model."""
    list_display = ['user', 'post', 'relevance_score', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__email', 'post__title']
    readonly_fields = ['created_at', 'read_at']


# Search Models

@admin.register(SearchIndex)
class SearchIndexAdmin(admin.ModelAdmin):
    """Admin for SearchIndex model."""
    list_display = ['name', 'organization_type', 'category', 'member_count', 'is_active', 'is_approved']
    list_filter = ['organization_type', 'is_active', 'is_approved', 'created_at']
    search_fields = ['name', 'description', 'category', 'tags']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Organization Info', {
            'fields': ('organization_type', 'organization_id', 'name', 'description', 'category', 'tags')
        }),
        ('Status', {
            'fields': ('is_active', 'is_approved', 'member_count')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(PopularSearch)
class PopularSearchAdmin(admin.ModelAdmin):
    """Admin for PopularSearch model."""
    list_display = ['query', 'search_count', 'last_searched']
    list_filter = ['last_searched']
    search_fields = ['query']
    readonly_fields = ['last_searched']
    ordering = ['-search_count']
