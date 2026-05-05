"""
Follow-related views and mixins for organizations.

Provides follow/unfollow functionality for all organization types.
"""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from apps.organizations.models import UserFollowOrganization, UserInterestOrganization
import logging

logger = logging.getLogger(__name__)


class OrganizationFollowMixin:
    """
    Mixin to add follow/unfollow functionality to organization viewsets.

    Adds actions:
    - follow(): Follow an organization
    - unfollow(): Unfollow an organization
    - followers(): List followers
    - is_following(): Check if user follows
    - express_interest(): Express interest in joining
    - withdraw_interest(): Withdraw interest
    """

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """
        Follow an organization.

        Returns:
            - success: Whether follow was successful
            - message: Status message
            - already_following: True if already following
        """
        organization = self.get_object()
        user = request.user

        # Get content type for this organization
        content_type = ContentType.objects.get_for_model(organization)

        try:
            # Create follow relationship
            follow, created = UserFollowOrganization.objects.get_or_create(
                user=user,
                content_type=content_type,
                object_id=organization.id,
                defaults={
                    'notify_on_posts': True,
                    'notify_on_events': True,
                }
            )

            if created:
                logger.info(f"User {user.email} followed {organization.name}")
                return Response({
                    'success': True,
                    'message': f'Successfully followed {organization.name}',
                    'already_following': False
                })
            else:
                return Response({
                    'success': True,
                    'message': f'Already following {organization.name}',
                    'already_following': True
                })

        except Exception as e:
            logger.error(f"Failed to follow organization: {e}")
            return Response({
                'success': False,
                'message': 'Failed to follow organization'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """
        Unfollow an organization.

        Returns:
            - success: Whether unfollow was successful
            - message: Status message
        """
        organization = self.get_object()
        user = request.user

        content_type = ContentType.objects.get_for_model(organization)

        deleted_count, _ = UserFollowOrganization.objects.filter(
            user=user,
            content_type=content_type,
            object_id=organization.id
        ).delete()

        if deleted_count > 0:
            logger.info(f"User {user.email} unfollowed {organization.name}")
            return Response({
                'success': True,
                'message': f'Successfully unfollowed {organization.name}'
            })
        else:
            return Response({
                'success': False,
                'message': f'You are not following {organization.name}'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        """
        List followers of an organization.

        Returns:
            - count: Number of followers
            - followers: List of follower details
        """
        organization = self.get_object()
        content_type = ContentType.objects.get_for_model(organization)

        followers = UserFollowOrganization.objects.filter(
            content_type=content_type,
            object_id=organization.id
        ).select_related('user')

        followers_data = [
            {
                'id': str(follow.user.id),
                'email': follow.user.email,
                'full_name': follow.user.get_full_name(),
                'followed_at': follow.created_at,
            }
            for follow in followers
        ]

        return Response({
            'count': len(followers_data),
            'followers': followers_data
        })

    @action(detail=True, methods=['get'])
    def is_following(self, request, pk=None):
        """
        Check if current user follows this organization.

        Returns:
            - is_following: Boolean
            - notify_on_posts: Notification preference
            - notify_on_events: Notification preference
        """
        organization = self.get_object()
        user = request.user

        content_type = ContentType.objects.get_for_model(organization)

        try:
            follow = UserFollowOrganization.objects.get(
                user=user,
                content_type=content_type,
                object_id=organization.id
            )
            return Response({
                'is_following': True,
                'notify_on_posts': follow.notify_on_posts,
                'notify_on_events': follow.notify_on_events,
            })
        except UserFollowOrganization.DoesNotExist:
            return Response({
                'is_following': False,
                'notify_on_posts': False,
                'notify_on_events': False,
            })

    @action(detail=True, methods=['post'])
    def express_interest(self, request, pk=None):
        """
        Express interest in joining an organization.

        Body params:
            - interest_level: low, medium, high (default: medium)
            - notes: Optional notes

        Returns:
            - success: Whether interest was recorded
            - message: Status message
        """
        organization = self.get_object()
        user = request.user

        interest_level = request.data.get('interest_level', 'medium')
        notes = request.data.get('notes', '')

        content_type = ContentType.objects.get_for_model(organization)

        try:
            interest, created = UserInterestOrganization.objects.update_or_create(
                user=user,
                content_type=content_type,
                object_id=organization.id,
                defaults={
                    'interest_level': interest_level,
                    'notes': notes,
                }
            )

            if created:
                logger.info(f"User {user.email} expressed interest in {organization.name}")
                return Response({
                    'success': True,
                    'message': f'Interest in {organization.name} recorded',
                    'created': True
                })
            else:
                logger.info(f"User {user.email} updated interest in {organization.name}")
                return Response({
                    'success': True,
                    'message': f'Interest in {organization.name} updated',
                    'created': False
                })

        except Exception as e:
            logger.error(f"Failed to record interest: {e}")
            return Response({
                'success': False,
                'message': 'Failed to record interest'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def withdraw_interest(self, request, pk=None):
        """
        Withdraw interest in an organization.

        Returns:
            - success: Whether interest was withdrawn
            - message: Status message
        """
        organization = self.get_object()
        user = request.user

        content_type = ContentType.objects.get_for_model(organization)

        deleted_count, _ = UserInterestOrganization.objects.filter(
            user=user,
            content_type=content_type,
            object_id=organization.id
        ).delete()

        if deleted_count > 0:
            logger.info(f"User {user.email} withdrew interest in {organization.name}")
            return Response({
                'success': True,
                'message': f'Interest in {organization.name} withdrawn'
            })
        else:
            return Response({
                'success': False,
                'message': f'No interest record found for {organization.name}'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def interested_users(self, request, pk=None):
        """
        List users interested in this organization (admin only).

        Query params:
            - interest_level: Filter by interest level
            - contacted: Filter by contacted status

        Returns:
            - count: Number of interested users
            - users: List of user details with interest info
        """
        organization = self.get_object()

        # Only admins can view interested users
        # Add permission check here based on your RBAC system

        content_type = ContentType.objects.get_for_model(organization)

        interests = UserInterestOrganization.objects.filter(
            content_type=content_type,
            object_id=organization.id
        ).select_related('user')

        # Apply filters
        interest_level = request.query_params.get('interest_level')
        if interest_level:
            interests = interests.filter(interest_level=interest_level)

        contacted = request.query_params.get('contacted')
        if contacted is not None:
            interests = interests.filter(contacted=contacted.lower() == 'true')

        users_data = [
            {
                'id': str(interest.user.id),
                'email': interest.user.email,
                'full_name': interest.user.get_full_name(),
                'interest_level': interest.interest_level,
                'notes': interest.notes,
                'contacted': interest.contacted,
                'contacted_at': interest.contacted_at,
                'created_at': interest.created_at,
            }
            for interest in interests
        ]

        return Response({
            'count': len(users_data),
            'users': users_data
        })
