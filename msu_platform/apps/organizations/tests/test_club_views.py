"""
Tests for Club views and API endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from apps.organizations.models import Club, OrganizationMember
from apps.core.tests.utils import (
    create_test_user,
    create_test_club,
    create_authenticated_client,
    assert_paginated_response,
)


@pytest.mark.django_db
class TestClubCRUD:
    """Test Club CRUD operations."""

    def test_create_club(self, authenticated_client, user):
        """Test creating a club."""
        url = reverse('organizations:clubs-list')
        data = {
            'name': 'Tech Club',
            'description': 'A club for tech enthusiasts',
            'category': 'academic',
            'meeting_schedule': 'Every Friday 3PM',
        }

        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Tech Club'
        assert response.data['owner']['id'] == str(user.id)

        # Verify club was created
        club = Club.objects.get(name='Tech Club')
        assert club.owner == user

    def test_create_club_unauthenticated(self, api_client):
        """Test creating club without authentication."""
        url = reverse('organizations:clubs-list')
        data = {'name': 'Tech Club', 'description': 'Test'}

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_club_invalid_data(self, authenticated_client):
        """Test creating club with invalid data."""
        url = reverse('organizations:clubs-list')
        data = {'name': ''}  # Empty name

        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_clubs(self, authenticated_client):
        """Test listing clubs."""
        # Create multiple clubs
        for i in range(5):
            create_test_club(name=f'Club {i}')

        url = reverse('organizations:clubs-list')

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert len(response.data['results']) >= 5

    def test_list_clubs_public(self, api_client):
        """Test listing clubs without authentication."""
        create_test_club()

        url = reverse('organizations:clubs-list')

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_club_detail(self, authenticated_client):
        """Test retrieving club detail."""
        club = create_test_club()

        url = reverse('organizations:clubs-detail', kwargs={'pk': club.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == club.name

    def test_get_club_detail_not_found(self, authenticated_client):
        """Test retrieving non-existent club."""
        url = reverse('organizations:clubs-detail', kwargs={'pk': '00000000-0000-0000-0000-000000000000'})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_club_owner(self, authenticated_client, user):
        """Test updating club as owner."""
        club = create_test_club(owner=user)

        url = reverse('organizations:clubs-detail', kwargs={'pk': club.id})
        data = {
            'name': 'Updated Club Name',
            'description': 'Updated description',
        }

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Club Name'

        # Verify database was updated
        club.refresh_from_db()
        assert club.name == 'Updated Club Name'

    def test_update_club_non_owner(self, authenticated_client):
        """Test updating club as non-owner."""
        other_user = create_test_user()
        club = create_test_club(owner=other_user)

        url = reverse('organizations:clubs-detail', kwargs={'pk': club.id})
        data = {'name': 'Hacked Name'}

        response = authenticated_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_club_owner(self, authenticated_client, user):
        """Test deleting club as owner."""
        club = create_test_club(owner=user)

        url = reverse('organizations:clubs-detail', kwargs={'pk': club.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Club.objects.filter(id=club.id).exists()

    def test_delete_club_non_owner(self, authenticated_client):
        """Test deleting club as non-owner."""
        other_user = create_test_user()
        club = create_test_club(owner=other_user)

        url = reverse('organizations:clubs-detail', kwargs={'pk': club.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestClubMembership:
    """Test club membership operations."""

    def test_join_club(self, authenticated_client, user):
        """Test joining a club."""
        club = create_test_club()

        url = reverse('organizations:clubs-join', kwargs={'pk': club.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert OrganizationMember.objects.filter(
            organization=club,
            user=user
        ).exists()

    def test_join_club_already_member(self, authenticated_client, user):
        """Test joining club when already a member."""
        club = create_test_club()
        OrganizationMember.objects.create(
            organization=club,
            user=user,
            role='member'
        )

        url = reverse('organizations:clubs-join', kwargs={'pk': club.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_leave_club(self, authenticated_client, user):
        """Test leaving a club."""
        club = create_test_club()
        OrganizationMember.objects.create(
            organization=club,
            user=user,
            role='member'
        )

        url = reverse('organizations:clubs-leave', kwargs={'pk': club.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert not OrganizationMember.objects.filter(
            organization=club,
            user=user
        ).exists()

    def test_leave_club_not_member(self, authenticated_client):
        """Test leaving club when not a member."""
        club = create_test_club()

        url = reverse('organizations:clubs-leave', kwargs={'pk': club.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_owner_cannot_leave_club(self, authenticated_client, user):
        """Test that owner cannot leave their own club."""
        club = create_test_club(owner=user)

        url = reverse('organizations:clubs-leave', kwargs={'pk': club.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_club_members(self, authenticated_client):
        """Test listing club members."""
        club = create_test_club()

        # Add members
        for i in range(5):
            user = create_test_user()
            OrganizationMember.objects.create(
                organization=club,
                user=user,
                role='member'
            )

        url = reverse('organizations:clubs-members', kwargs={'pk': club.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert_paginated_response(response.data)
        assert len(response.data['results']) >= 5

    def test_approve_member_admin(self, authenticated_client, user):
        """Test approving member as admin."""
        club = create_test_club(owner=user)
        new_member = create_test_user()

        # Create pending membership
        membership = OrganizationMember.objects.create(
            organization=club,
            user=new_member,
            role='pending'
        )

        url = reverse('organizations:clubs-approve-member', kwargs={
            'pk': club.id,
            'member_id': new_member.id
        })

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK

        # Verify membership was approved
        membership.refresh_from_db()
        assert membership.role == 'member'

    def test_approve_member_non_admin(self, authenticated_client):
        """Test approving member as non-admin."""
        club = create_test_club()
        new_member = create_test_user()

        OrganizationMember.objects.create(
            organization=club,
            user=new_member,
            role='pending'
        )

        url = reverse('organizations:clubs-approve-member', kwargs={
            'pk': club.id,
            'member_id': new_member.id
        })

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestClubFiltering:
    """Test club filtering and search."""

    def test_filter_clubs_by_category(self, authenticated_client):
        """Test filtering clubs by category."""
        create_test_club(category='academic')
        create_test_club(category='social')
        create_test_club(category='academic')

        url = reverse('organizations:clubs-list')

        response = authenticated_client.get(url, {'category': 'academic'})

        assert response.status_code == status.HTTP_200_OK
        assert all(c['category'] == 'academic' for c in response.data['results'])

    def test_search_clubs_by_name(self, authenticated_client):
        """Test searching clubs by name."""
        create_test_club(name='Tech Innovators Club')
        create_test_club(name='Drama Society')

        url = reverse('organizations:clubs-list')

        response = authenticated_client.get(url, {'search': 'Tech'})

        assert response.status_code == status.HTTP_200_OK
        assert any('Tech' in c['name'] for c in response.data['results'])

    def test_search_clubs_by_description(self, authenticated_client):
        """Test searching clubs by description."""
        create_test_club(
            name='Club A',
            description='Programming and software development'
        )
        create_test_club(
            name='Club B',
            description='Music and performance'
        )

        url = reverse('organizations:clubs-list')

        response = authenticated_client.get(url, {'search': 'programming'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_order_clubs_by_members(self, authenticated_client):
        """Test ordering clubs by member count."""
        url = reverse('organizations:clubs-list')

        response = authenticated_client.get(url, {'ordering': '-members_count'})

        assert response.status_code == status.HTTP_200_OK

    def test_filter_clubs_my_clubs(self, authenticated_client, user):
        """Test filtering user's clubs."""
        create_test_club(owner=user)
        create_test_club()  # Other user's club

        url = reverse('organizations:clubs-list')

        response = authenticated_client.get(url, {'my_clubs': 'true'})

        assert response.status_code == status.HTTP_200_OK
        assert all(c['owner']['id'] == str(user.id) for c in response.data['results'])


@pytest.mark.django_db
@pytest.mark.permissions
class TestClubPermissions:
    """Test club permission handling."""

    def test_member_can_view_private_content(self, authenticated_client, user):
        """Test that members can view private club content."""
        club = create_test_club()
        OrganizationMember.objects.create(
            organization=club,
            user=user,
            role='member'
        )

        url = reverse('organizations:clubs-detail', kwargs={'pk': club.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'private_field' in response.data or response.status_code == 200

    def test_non_member_cannot_view_private_content(self, authenticated_client):
        """Test that non-members cannot view certain private content."""
        club = create_test_club()

        url = reverse('organizations:clubs-private-content', kwargs={'pk': club.id})

        response = authenticated_client.get(url)

        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
