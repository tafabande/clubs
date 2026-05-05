"""
Add comprehensive performance indexes to organization models.

This migration adds database indexes to improve query performance for:
- Posts and feeds
- Comments, likes, and shares
- Organization lookups
- Memberships
- Follows and interests
- Search
"""
from django.db import migrations, models
from django.contrib.postgres.indexes import GinIndex


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_add_search_vector'),
    ]

    operations = [
        # ===== Post Model Indexes =====
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-created_at'], name='posts_created_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['content_type', 'object_id'], name='posts_org_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['author', '-created_at'], name='posts_author_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['post_type', '-created_at'], name='posts_type_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['is_pinned', '-created_at'], name='posts_pinned_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['visibility', '-created_at'], name='posts_visibility_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['is_active', '-created_at'], name='posts_active_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['content_type', 'object_id', '-created_at'], name='posts_org_created_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['event_date'], name='posts_event_date_idx'),
        ),

        # ===== PostMedia Indexes =====
        migrations.AddIndex(
            model_name='postmedia',
            index=models.Index(fields=['post', 'order'], name='post_media_post_order_idx'),
        ),
        migrations.AddIndex(
            model_name='postmedia',
            index=models.Index(fields=['media_type'], name='post_media_type_idx'),
        ),
        migrations.AddIndex(
            model_name='postmedia',
            index=models.Index(fields=['processing_status'], name='post_media_status_idx'),
        ),

        # ===== PostLike Indexes =====
        migrations.AddIndex(
            model_name='postlike',
            index=models.Index(fields=['post', 'user'], name='post_likes_post_user_idx'),
        ),
        migrations.AddIndex(
            model_name='postlike',
            index=models.Index(fields=['post', '-created_at'], name='post_likes_post_idx'),
        ),
        migrations.AddIndex(
            model_name='postlike',
            index=models.Index(fields=['user', '-created_at'], name='post_likes_user_idx'),
        ),

        # ===== PostComment Indexes =====
        migrations.AddIndex(
            model_name='postcomment',
            index=models.Index(fields=['post', '-created_at'], name='post_comments_post_idx'),
        ),
        migrations.AddIndex(
            model_name='postcomment',
            index=models.Index(fields=['user', '-created_at'], name='post_comments_user_idx'),
        ),
        migrations.AddIndex(
            model_name='postcomment',
            index=models.Index(fields=['parent', '-created_at'], name='post_comments_parent_idx'),
        ),
        migrations.AddIndex(
            model_name='postcomment',
            index=models.Index(fields=['is_active', '-created_at'], name='post_comments_active_idx'),
        ),

        # ===== PostShare Indexes =====
        migrations.AddIndex(
            model_name='postshare',
            index=models.Index(fields=['post', '-created_at'], name='post_shares_post_idx'),
        ),
        migrations.AddIndex(
            model_name='postshare',
            index=models.Index(fields=['user', '-created_at'], name='post_shares_user_idx'),
        ),

        # ===== Feed Indexes =====
        migrations.AddIndex(
            model_name='feed',
            index=models.Index(fields=['user', '-created_at'], name='feeds_user_created_idx'),
        ),
        migrations.AddIndex(
            model_name='feed',
            index=models.Index(fields=['user', '-relevance_score'], name='feeds_user_score_idx'),
        ),
        migrations.AddIndex(
            model_name='feed',
            index=models.Index(fields=['user', 'is_read', '-relevance_score'], name='feeds_user_read_score_idx'),
        ),
        migrations.AddIndex(
            model_name='feed',
            index=models.Index(fields=['is_read', '-created_at'], name='feeds_read_idx'),
        ),
        migrations.AddIndex(
            model_name='feed',
            index=models.Index(fields=['source_type', '-created_at'], name='feeds_source_idx'),
        ),
        migrations.AddIndex(
            model_name='feed',
            index=models.Index(fields=['post', 'user'], name='feeds_post_user_idx'),
        ),

        # ===== UserFollowOrganization Indexes =====
        migrations.AddIndex(
            model_name='userfolloworganization',
            index=models.Index(fields=['user', '-created_at'], name='follow_org_user_idx'),
        ),
        migrations.AddIndex(
            model_name='userfolloworganization',
            index=models.Index(fields=['content_type', 'object_id', '-created_at'], name='follow_org_ct_idx'),
        ),
        migrations.AddIndex(
            model_name='userfolloworganization',
            index=models.Index(fields=['user', 'content_type'], name='follow_org_user_ct_idx'),
        ),
        migrations.AddIndex(
            model_name='userfolloworganization',
            index=models.Index(fields=['user', 'notify_on_posts'], name='follow_org_notify_posts_idx'),
        ),
        migrations.AddIndex(
            model_name='userfolloworganization',
            index=models.Index(fields=['user', 'notify_on_events'], name='follow_org_notify_events_idx'),
        ),

        # ===== UserInterestOrganization Indexes =====
        migrations.AddIndex(
            model_name='userinterestorganization',
            index=models.Index(fields=['user', '-created_at'], name='interest_org_user_idx'),
        ),
        migrations.AddIndex(
            model_name='userinterestorganization',
            index=models.Index(fields=['content_type', 'object_id', '-created_at'], name='interest_org_ct_idx'),
        ),
        migrations.AddIndex(
            model_name='userinterestorganization',
            index=models.Index(fields=['interest_level', '-created_at'], name='interest_org_level_idx'),
        ),
        migrations.AddIndex(
            model_name='userinterestorganization',
            index=models.Index(fields=['contacted', '-created_at'], name='interest_org_contacted_idx'),
        ),
        migrations.AddIndex(
            model_name='userinterestorganization',
            index=models.Index(fields=['content_type', 'object_id', 'contacted'], name='interest_org_ct_contacted_idx'),
        ),

        # ===== SearchIndex Indexes (additional to GIN) =====
        migrations.AddIndex(
            model_name='searchindex',
            index=models.Index(fields=['organization_type', 'is_active'], name='search_type_active_idx'),
        ),
        migrations.AddIndex(
            model_name='searchindex',
            index=models.Index(fields=['is_active', 'is_approved', '-member_count'], name='search_status_count_idx'),
        ),
        migrations.AddIndex(
            model_name='searchindex',
            index=models.Index(fields=['category', '-member_count'], name='search_category_idx'),
        ),
        migrations.AddIndex(
            model_name='searchindex',
            index=models.Index(fields=['organization_id'], name='search_org_id_idx'),
        ),
        migrations.AddIndex(
            model_name='searchindex',
            index=models.Index(fields=['organization_type', 'organization_id'], name='search_org_type_id_idx'),
        ),

        # ===== PopularSearch Indexes =====
        migrations.AddIndex(
            model_name='popularsearch',
            index=models.Index(fields=['-search_count'], name='popular_search_count_idx'),
        ),
        migrations.AddIndex(
            model_name='popularsearch',
            index=models.Index(fields=['-last_searched'], name='popular_search_date_idx'),
        ),
        migrations.AddIndex(
            model_name='popularsearch',
            index=models.Index(fields=['query'], name='popular_search_query_idx'),
        ),

        # ===== Club Indexes =====
        migrations.AddIndex(
            model_name='club',
            index=models.Index(fields=['is_active', 'is_approved'], name='clubs_status_idx'),
        ),
        migrations.AddIndex(
            model_name='club',
            index=models.Index(fields=['category', 'is_active'], name='clubs_category_idx'),
        ),
        migrations.AddIndex(
            model_name='club',
            index=models.Index(fields=['created_by'], name='clubs_creator_idx'),
        ),
        migrations.AddIndex(
            model_name='club',
            index=models.Index(fields=['-created_at'], name='clubs_created_idx'),
        ),
        migrations.AddIndex(
            model_name='club',
            index=models.Index(fields=['is_approved', '-created_at'], name='clubs_approved_created_idx'),
        ),

        # ===== ClubMembership Indexes =====
        migrations.AddIndex(
            model_name='clubmembership',
            index=models.Index(fields=['club', 'status'], name='club_membership_club_status_idx'),
        ),
        migrations.AddIndex(
            model_name='clubmembership',
            index=models.Index(fields=['user', 'status'], name='club_membership_user_status_idx'),
        ),
        migrations.AddIndex(
            model_name='clubmembership',
            index=models.Index(fields=['status', '-joined_at'], name='club_membership_status_joined_idx'),
        ),

        # ===== Church Indexes =====
        migrations.AddIndex(
            model_name='church',
            index=models.Index(fields=['is_active', 'is_approved'], name='churches_status_idx'),
        ),
        migrations.AddIndex(
            model_name='church',
            index=models.Index(fields=['denomination', 'is_active'], name='churches_denomination_idx'),
        ),
        migrations.AddIndex(
            model_name='church',
            index=models.Index(fields=['created_by'], name='churches_creator_idx'),
        ),
        migrations.AddIndex(
            model_name='church',
            index=models.Index(fields=['-created_at'], name='churches_created_idx'),
        ),

        # ===== ChurchMembership Indexes =====
        migrations.AddIndex(
            model_name='churchmembership',
            index=models.Index(fields=['church', 'status'], name='church_membership_church_status_idx'),
        ),
        migrations.AddIndex(
            model_name='churchmembership',
            index=models.Index(fields=['user', 'status'], name='church_membership_user_status_idx'),
        ),

        # ===== SportsTeam Indexes =====
        migrations.AddIndex(
            model_name='sportsteam',
            index=models.Index(fields=['is_active', 'is_approved'], name='sports_status_idx'),
        ),
        migrations.AddIndex(
            model_name='sportsteam',
            index=models.Index(fields=['sport_type', 'is_active'], name='sports_type_idx'),
        ),
        migrations.AddIndex(
            model_name='sportsteam',
            index=models.Index(fields=['division', 'sport_type'], name='sports_division_type_idx'),
        ),
        migrations.AddIndex(
            model_name='sportsteam',
            index=models.Index(fields=['created_by'], name='sports_creator_idx'),
        ),
        migrations.AddIndex(
            model_name='sportsteam',
            index=models.Index(fields=['-created_at'], name='sports_created_idx'),
        ),

        # ===== SportsTeamMembership Indexes =====
        migrations.AddIndex(
            model_name='sportsteammembership',
            index=models.Index(fields=['sports_team', 'status'], name='sports_membership_team_status_idx'),
        ),
        migrations.AddIndex(
            model_name='sportsteammembership',
            index=models.Index(fields=['user', 'status'], name='sports_membership_user_status_idx'),
        ),

        # ===== Activity Indexes =====
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['is_active', 'is_approved'], name='activities_status_idx'),
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['activity_type', 'is_active'], name='activities_type_idx'),
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['start_date'], name='activities_start_date_idx'),
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['end_date'], name='activities_end_date_idx'),
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['registration_deadline'], name='activities_reg_deadline_idx'),
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['is_recurring', 'start_date'], name='activities_recurring_idx'),
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['created_by'], name='activities_creator_idx'),
        ),

        # ===== ActivityRegistration Indexes =====
        migrations.AddIndex(
            model_name='activityregistration',
            index=models.Index(fields=['activity', 'status'], name='activity_reg_activity_status_idx'),
        ),
        migrations.AddIndex(
            model_name='activityregistration',
            index=models.Index(fields=['user', 'status'], name='activity_reg_user_status_idx'),
        ),
        migrations.AddIndex(
            model_name='activityregistration',
            index=models.Index(fields=['-registered_at'], name='activity_reg_registered_idx'),
        ),
    ]
