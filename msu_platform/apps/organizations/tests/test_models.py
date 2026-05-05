"""
Tests for Organization models.
"""
import pytest
from django.utils import timezone
from datetime import timedelta
from apps.organizations.models import (
    Club,
    Church,
    SportsTeam,
    Activity,
    Post,
    Comment,
    OrganizationFollow,
    Interest,
)
from apps.core.tests.utils import (
    create_test_user,
    create_test_club,
    create_test_church,
    create_test_sports_team,
    create_test_activity,
    create_test_post,
    create_test_comment,
)


@pytest.mark.django_db
class TestClubModel:
    """Test Club model."""

    def test_create_club(self):
        """Test creating a club."""
        user = create_test_user()
        club = create_test_club(
            owner=user,
            name="Tech Club",
            description="Technology enthusiasts club",
            category="academic",
        )

        assert club.name == "Tech Club"
        assert club.owner == user
        assert club.category == "academic"
        assert club.is_active is True

    def test_club_str_representation(self):
        """Test club string representation."""
        club = create_test_club(name="Tech Club")
        assert str(club) == "Tech Club"

    def test_club_slug_generation(self):
        """Test that slug is auto-generated."""
        club = create_test_club(name="Tech Club 2024")
        assert club.slug is not None
        assert "tech-club" in club.slug.lower()

    def test_club_members_count(self):
        """Test members count property."""
        club = create_test_club()
        user1 = create_test_user()
        user2 = create_test_user()

        club.members.add(user1, user2)

        assert club.members_count == 2

    def test_club_followers_count(self):
        """Test followers count property."""
        club = create_test_club()
        user1 = create_test_user()
        user2 = create_test_user()

        OrganizationFollow.objects.create(user=user1, organization=club)
        OrganizationFollow.objects.create(user=user2, organization=club)

        assert club.followers_count == 2


@pytest.mark.django_db
class TestChurchModel:
    """Test Church model."""

    def test_create_church(self):
        """Test creating a church."""
        user = create_test_user()
        church = create_test_church(
            owner=user,
            name="Grace Chapel",
            denomination="catholic",
            service_times="Sunday 10:00 AM",
        )

        assert church.name == "Grace Chapel"
        assert church.denomination == "catholic"
        assert church.service_times == "Sunday 10:00 AM"

    def test_church_denomination_choices(self):
        """Test church denomination field choices."""
        church = create_test_church(denomination="protestant")
        assert church.denomination == "protestant"


@pytest.mark.django_db
class TestSportsTeamModel:
    """Test SportsTeam model."""

    def test_create_sports_team(self):
        """Test creating a sports team."""
        user = create_test_user()
        team = create_test_sports_team(
            owner=user,
            name="MSU Football",
            sport_type="football",
            division="first",
        )

        assert team.name == "MSU Football"
        assert team.sport_type == "football"
        assert team.division == "first"

    def test_sports_team_with_coach(self):
        """Test sports team with coach information."""
        team = create_test_sports_team(
            sport_type="basketball",
            coach_name="John Coach",
            coach_email="coach@msu.ac.zw",
        )

        assert team.coach_name == "John Coach"
        assert team.coach_email == "coach@msu.ac.zw"


@pytest.mark.django_db
class TestActivityModel:
    """Test Activity model."""

    def test_create_activity(self):
        """Test creating an activity."""
        club = create_test_club()
        activity = create_test_activity(
            organization=club,
            title="Tech Workshop",
            location="Room 101",
            capacity=50,
        )

        assert activity.title == "Tech Workshop"
        assert activity.organization == club
        assert activity.capacity == 50

    def test_activity_with_registration(self):
        """Test activity registration."""
        activity = create_test_activity(capacity=10)
        user = create_test_user()

        activity.registered_users.add(user)

        assert activity.registered_users.count() == 1
        assert user in activity.registered_users.all()

    def test_activity_is_full(self):
        """Test activity capacity check."""
        activity = create_test_activity(capacity=2)

        user1 = create_test_user()
        user2 = create_test_user()

        activity.registered_users.add(user1, user2)

        assert activity.is_full is True

    def test_activity_registration_deadline(self):
        """Test activity registration deadline."""
        activity = create_test_activity(
            registration_deadline=timezone.now() + timedelta(days=7)
        )

        assert activity.can_register is True

    def test_activity_past_deadline(self):
        """Test activity past registration deadline."""
        activity = create_test_activity(
            registration_deadline=timezone.now() - timedelta(days=1)
        )

        assert activity.can_register is False


@pytest.mark.django_db
class TestPostModel:
    """Test Post model."""

    def test_create_text_post(self):
        """Test creating a text post."""
        user = create_test_user()
        club = create_test_club()
        post = create_test_post(
            author=user,
            organization=club,
            post_type="text",
            content="Hello World",
        )

        assert post.post_type == "text"
        assert post.content == "Hello World"
        assert post.author == user
        assert post.organization == club

    def test_post_types(self):
        """Test different post types."""
        post_types = ["text", "image", "video", "announcement", "event", "poll"]

        for post_type in post_types:
            post = create_test_post(post_type=post_type)
            assert post.post_type == post_type

    def test_post_visibility(self):
        """Test post visibility options."""
        public_post = create_test_post(visibility="public")
        members_post = create_test_post(visibility="members")
        private_post = create_test_post(visibility="private")

        assert public_post.visibility == "public"
        assert members_post.visibility == "members"
        assert private_post.visibility == "private"

    def test_post_likes_count(self):
        """Test post likes count."""
        post = create_test_post()
        user1 = create_test_user()
        user2 = create_test_user()

        post.likes.add(user1, user2)

        assert post.likes_count == 2

    def test_post_comments_count(self):
        """Test post comments count."""
        post = create_test_post()
        create_test_comment(post=post)
        create_test_comment(post=post)

        assert post.comments_count == 2


@pytest.mark.django_db
class TestCommentModel:
    """Test Comment model."""

    def test_create_comment(self):
        """Test creating a comment."""
        user = create_test_user()
        post = create_test_post()
        comment = create_test_comment(
            author=user,
            post=post,
            content="Great post!",
        )

        assert comment.author == user
        assert comment.post == post
        assert comment.content == "Great post!"

    def test_nested_comments(self):
        """Test nested comment replies."""
        post = create_test_post()
        parent_comment = create_test_comment(post=post, content="Parent comment")
        reply = create_test_comment(
            post=post,
            content="Reply to parent",
            parent=parent_comment,
        )

        assert reply.parent == parent_comment
        assert parent_comment.replies.count() == 1

    def test_comment_depth_level(self):
        """Test comment nesting depth."""
        post = create_test_post()
        level1 = create_test_comment(post=post)
        level2 = create_test_comment(post=post, parent=level1)
        level3 = create_test_comment(post=post, parent=level2)

        assert level1.parent is None
        assert level2.parent == level1
        assert level3.parent == level2


@pytest.mark.django_db
class TestOrganizationFollowModel:
    """Test OrganizationFollow model."""

    def test_create_follow(self):
        """Test creating an organization follow."""
        user = create_test_user()
        club = create_test_club()

        follow = OrganizationFollow.objects.create(
            user=user,
            organization=club,
        )

        assert follow.user == user
        assert follow.organization == club

    def test_unique_follow_constraint(self):
        """Test that follow relationship must be unique."""
        user = create_test_user()
        club = create_test_club()

        OrganizationFollow.objects.create(user=user, organization=club)

        with pytest.raises(Exception):  # IntegrityError
            OrganizationFollow.objects.create(user=user, organization=club)


@pytest.mark.django_db
class TestInterestModel:
    """Test Interest model."""

    def test_create_interest(self):
        """Test creating an interest."""
        user = create_test_user()
        club = create_test_club()

        interest = Interest.objects.create(
            user=user,
            organization=club,
        )

        assert interest.user == user
        assert interest.organization == club

    def test_unique_interest_constraint(self):
        """Test that interest must be unique."""
        user = create_test_user()
        club = create_test_club()

        Interest.objects.create(user=user, organization=club)

        with pytest.raises(Exception):  # IntegrityError
            Interest.objects.create(user=user, organization=club)
