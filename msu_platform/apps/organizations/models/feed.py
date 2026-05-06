"""
Social feed models for organizations.

Allows organizations to post updates, events, media, and announcements
similar to Facebook feeds.
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.users.models import User
from apps.core.validators import validate_image_file, FileSizeValidator, MimeTypeValidator
import uuid


class Post(models.Model):
    """
    Social media post by an organization.

    Features:
    - Text content
    - Media attachments (images, videos)
    - Post types (announcement, event, achievement, general)
    - Visibility controls
    - Engagement tracking (likes, comments)
    """

    POST_TYPES = [
        ('announcement', 'Announcement'),
        ('event', 'Event'),
        ('achievement', 'Achievement'),
        ('general', 'General Update'),
        ('media', 'Media Post'),
        ('recruitment', 'Recruitment'),
    ]

    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('members_only', 'Members Only'),
        ('followers_only', 'Followers Only'),
        ('admin_only', 'Admin Only'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Organization that created the post (generic FK)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text='Type of organization (Club, Church, Sports Team, Activity)'
    )
    object_id = models.UUIDField(help_text='ID of the organization')
    organization = GenericForeignKey('content_type', 'object_id')

    # Author
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text='User who created the post'
    )

    # Content
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='general')
    title = models.CharField(max_length=200, blank=True, help_text='Optional title for post')
    content = models.TextField(help_text='Post content/description')

    # Media
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True, validators=[validate_image_file])
    video = models.FileField(
        upload_to='posts/videos/', 
        blank=True, 
        null=True, 
        validators=[
            FileSizeValidator(max_size=100 * 1024 * 1024),  # 100MB for video
            MimeTypeValidator(allowed_types=['video/mp4', 'video/mpeg', 'video/quicktime', 'video/x-msvideo'])
        ]
    )
    video_thumbnail = models.ImageField(upload_to='posts/thumbnails/', blank=True, null=True, help_text='Auto-generated video thumbnail', validators=[validate_image_file])

    # Event details (if post_type is 'event')
    event_date = models.DateTimeField(null=True, blank=True, help_text='Event date and time')
    event_location = models.CharField(max_length=200, blank=True, help_text='Event location')
    event_link = models.URLField(blank=True, help_text='Event registration or info link')

    # Visibility
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    is_pinned = models.BooleanField(default=False, help_text='Pin post to top of feed')

    # Engagement tracking
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # Tags for search
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags')

    class Meta:
        db_table = 'posts'
        ordering = ['-is_pinned', '-created_at']
        indexes = [
            models.Index(fields=['-created_at'], name='posts_created_idx'),
            models.Index(fields=['content_type', 'object_id'], name='posts_org_idx'),
            models.Index(fields=['author', '-created_at'], name='posts_author_idx'),
            models.Index(fields=['post_type', '-created_at'], name='posts_type_idx'),
            models.Index(fields=['is_pinned', '-created_at'], name='posts_pinned_idx'),
            models.Index(fields=['visibility', '-created_at'], name='posts_visibility_idx'),
            models.Index(fields=['is_active', '-created_at'], name='posts_active_idx'),
            models.Index(fields=['content_type', 'object_id', '-created_at'], name='posts_org_created_idx'),
            models.Index(fields=['event_date'], name='posts_event_date_idx'),
        ]

    def __str__(self):
        org_name = str(self.organization) if self.organization else 'Unknown'
        return f"{org_name} - {self.get_post_type_display()} - {self.created_at.strftime('%Y-%m-%d')}"

    @property
    def organization_name(self):
        """Return organization name."""
        return str(self.organization) if self.organization else ''

    @property
    def organization_type(self):
        """Return organization type."""
        if self.content_type:
            return self.content_type.model
        return ''


class PostMedia(models.Model):
    """
    Additional media attachments for posts.
    Allows multiple images/videos per post.
    """

    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')

    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    file = models.FileField(
        upload_to='posts/media/',
        validators=[
            FileSizeValidator(max_size=100 * 1024 * 1024),
        ]
    )
    caption = models.CharField(max_length=500, blank=True)

    # CDN & Processing fields
    file_size = models.BigIntegerField(default=0, help_text='File size in bytes')
    processing_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending',
        help_text='Video transcoding status'
    )
    transcoded_versions = models.JSONField(
        default=dict,
        blank=True,
        help_text='URLs of transcoded video versions (360p, 720p, 1080p)'
    )

    order = models.IntegerField(default=0, help_text='Display order')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_media'
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['post', 'order'], name='post_media_post_order_idx'),
            models.Index(fields=['media_type'], name='post_media_type_idx'),
            models.Index(fields=['processing_status'], name='post_media_status_idx'),
        ]

    def __str__(self):
        return f"{self.get_media_type_display()} for {self.post.id}"


class PostLike(models.Model):
    """Track users who liked a post."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_likes'
        unique_together = ['post', 'user']
        indexes = [
            models.Index(fields=['post', 'user'], name='post_likes_post_user_idx'),
            models.Index(fields=['post', '-created_at'], name='post_likes_post_idx'),
            models.Index(fields=['user', '-created_at'], name='post_likes_user_idx'),
        ]

    def __str__(self):
        return f"{self.user.email} liked post {self.post.id}"


class PostComment(models.Model):
    """Comments on posts."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')

    content = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        help_text='Parent comment for nested replies'
    )

    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'post_comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', '-created_at'], name='post_comments_post_idx'),
            models.Index(fields=['user', '-created_at'], name='post_comments_user_idx'),
            models.Index(fields=['parent', '-created_at'], name='post_comments_parent_idx'),
            models.Index(fields=['is_active', '-created_at'], name='post_comments_active_idx'),
        ]

    def __str__(self):
        return f"Comment by {self.user.email} on {self.post.id}"


class PostShare(models.Model):
    """Track post shares."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_shares')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_shares'
        indexes = [
            models.Index(fields=['post', '-created_at'], name='post_shares_post_idx'),
            models.Index(fields=['user', '-created_at'], name='post_shares_user_idx'),
        ]

    def __str__(self):
        return f"{self.user.email} shared post {self.post.id}"


class Feed(models.Model):
    """
    User's personalized feed.

    Aggregates posts from organizations the user follows/is a member of.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feeds')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # Enhanced relevance scoring
    relevance_score = models.FloatField(default=1.0, help_text='Overall relevance score (0-100)')
    engagement_score = models.FloatField(default=0.0, help_text='Score based on likes, comments, shares')
    recency_score = models.FloatField(default=0.0, help_text='Score based on post age')
    relationship_score = models.FloatField(default=0.0, help_text='Score based on user-org relationship')
    priority_boost = models.FloatField(default=0.0, help_text='Manual priority adjustment')

    # Source tracking
    source_type = models.CharField(
        max_length=20,
        choices=[
            ('following', 'Following'),
            ('member', 'Member'),
            ('interest', 'Interest'),
            ('recommended', 'Recommended'),
            ('trending', 'Trending'),
        ],
        default='following',
        help_text='How this post entered the feed'
    )

    # Tracking
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_scored_at = models.DateTimeField(auto_now=True, help_text='Last time score was updated')

    class Meta:
        db_table = 'feeds'
        ordering = ['-relevance_score', '-created_at']
        unique_together = ['user', 'post']
        indexes = [
            models.Index(fields=['user', '-created_at'], name='feeds_user_created_idx'),
            models.Index(fields=['user', '-relevance_score'], name='feeds_user_score_idx'),
            models.Index(fields=['user', 'is_read', '-relevance_score'], name='feeds_user_read_score_idx'),
            models.Index(fields=['is_read', '-created_at'], name='feeds_read_idx'),
            models.Index(fields=['source_type', '-created_at'], name='feeds_source_idx'),
            models.Index(fields=['post', 'user'], name='feeds_post_user_idx'),
        ]

    def __str__(self):
        return f"Feed item for {self.user.email}"
