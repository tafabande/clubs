"""
Serializers for social feed functionality.
"""
from rest_framework import serializers
from apps.organizations.models import (
    Post, PostMedia, PostLike, PostComment, PostShare, Feed
)
from apps.users.serializers import UserSerializer


class PostMediaSerializer(serializers.ModelSerializer):
    """Serializer for post media attachments."""

    class Meta:
        model = PostMedia
        fields = ['id', 'media_type', 'file', 'caption', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']


class PostCommentSerializer(serializers.ModelSerializer):
    """Serializer for post comments."""

    user = UserSerializer(read_only=True)
    replies_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = [
            'id', 'user', 'content', 'parent', 'likes_count',
            'replies_count', 'user_has_liked', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'likes_count']

    def get_replies_count(self, obj):
        """Get count of replies to this comment."""
        return obj.replies.filter(is_active=True).count()

    def get_user_has_liked(self, obj):
        """Check if current user has liked this comment."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Would need CommentLike model for this
            return False
        return False


class PostSerializer(serializers.ModelSerializer):
    """Serializer for organization posts."""

    author = UserSerializer(read_only=True)
    organization_name = serializers.CharField(read_only=True)
    organization_type = serializers.CharField(read_only=True)
    media = PostMediaSerializer(many=True, read_only=True)
    user_has_liked = serializers.SerializerMethodField()
    user_has_shared = serializers.SerializerMethodField()
    recent_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'organization_name', 'organization_type',
            'content_type', 'object_id', 'post_type', 'title', 'content',
            'image', 'video', 'media', 'event_date', 'event_location',
            'event_link', 'visibility', 'is_pinned', 'likes_count',
            'comments_count', 'shares_count', 'user_has_liked',
            'user_has_shared', 'recent_comments', 'tags', 'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'organization_name', 'organization_type',
            'likes_count', 'comments_count', 'shares_count', 'created_at',
            'updated_at'
        ]

    def get_user_has_liked(self, obj):
        """Check if current user has liked this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(
                post=obj,
                user=request.user
            ).exists()
        return False

    def get_user_has_shared(self, obj):
        """Check if current user has shared this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostShare.objects.filter(
                post=obj,
                user=request.user
            ).exists()
        return False

    def get_recent_comments(self, obj):
        """Get recent comments for this post."""
        comments = obj.comments.filter(
            is_active=True,
            parent__isnull=True  # Only top-level comments
        ).order_by('-created_at')[:3]
        return PostCommentSerializer(comments, many=True, context=self.context).data


class CreatePostSerializer(serializers.ModelSerializer):
    """Serializer for creating posts."""

    media_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = [
            'content_type', 'object_id', 'post_type', 'title', 'content',
            'image', 'video', 'event_date', 'event_location', 'event_link',
            'visibility', 'tags', 'media_files'
        ]

    def create(self, validated_data):
        """Create post with media files."""
        media_files = validated_data.pop('media_files', [])
        post = Post.objects.create(**validated_data)

        # Create media attachments
        for idx, file in enumerate(media_files):
            # Determine media type from file extension
            file_ext = file.name.split('.')[-1].lower()
            if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                media_type = 'image'
            elif file_ext in ['mp4', 'webm', 'mov']:
                media_type = 'video'
            else:
                media_type = 'document'

            PostMedia.objects.create(
                post=post,
                media_type=media_type,
                file=file,
                order=idx
            )

        return post


class FeedSerializer(serializers.ModelSerializer):
    """Serializer for user's personalized feed."""

    post = PostSerializer(read_only=True)

    class Meta:
        model = Feed
        fields = [
            'id', 'post', 'relevance_score', 'is_read', 'read_at',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
