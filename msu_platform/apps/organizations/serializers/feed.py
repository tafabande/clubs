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
    organization = serializers.SerializerMethodField()
    media = PostMediaSerializer(many=True, read_only=True)
    user_has_liked = serializers.SerializerMethodField()
    user_has_shared = serializers.SerializerMethodField()
    recent_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'organization',
            'content_type', 'object_id', 'post_type', 'title', 'content',
            'image', 'video', 'media', 'event_date', 'event_location',
            'event_link', 'visibility', 'is_pinned', 'likes_count',
            'comments_count', 'shares_count', 'user_has_liked',
            'user_has_shared', 'recent_comments', 'tags', 'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'likes_count', 'comments_count', 
            'shares_count', 'created_at', 'updated_at'
        ]

    def get_organization(self, obj):
        """Return organization details."""
        org = obj.organization
        if not org:
            return None
        return {
            'id': str(org.id),
            'name': org.name,
            'type': obj.organization_type
        }

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

    organization_type = serializers.ChoiceField(
        choices=['club', 'church', 'sportsteam', 'activity'],
        write_only=True
    )
    organization_id = serializers.IntegerField(write_only=True)

    media_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = [
            'organization_type', 'organization_id', 'post_type', 'title', 'content',
            'image', 'video', 'event_date', 'event_location', 'event_link',
            'visibility', 'tags', 'media_files'
        ]

    def create(self, validated_data):
        """Create post with media files."""
        org_type_str = validated_data.pop('organization_type')
        org_id = validated_data.pop('organization_id')
        
        from django.contrib.contenttypes.models import ContentType
        from apps.organizations.models import Club, Church, SportsTeam, Activity
        
        model_map = {
            'club': Club,
            'church': Church,
            'sportsteam': SportsTeam,
            'activity': Activity
        }
        
        ct = ContentType.objects.get_for_model(model_map[org_type_str])
        validated_data['content_type'] = ct
        validated_data['object_id'] = org_id

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
