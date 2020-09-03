"""API Tests."""
from django.contrib.auth import get_user_model

import pytest
from rest_framework import status

from ..models import STT

User = get_user_model()


@pytest.mark.django_db
def test_retrieve_user(api_client, user):
    """Test user retrieval."""
    response = api_client.get(f"/v1/users/{user.pk}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user.username


@pytest.mark.django_db
def test_can_update_own_user(api_client, user):
    """Test a user can update their own user."""
    api_client.login(username=user.username, password="test_password")
    response = api_client.patch(f"/v1/users/{user.pk}/", {"first_name": "Jane"})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "Jane"
    assert User.objects.filter(first_name="Jane").exists()


@pytest.mark.django_db
def test_cannot_update_user_anonymously(api_client, user):
    """Test an unauthenticated user cannot update a user."""
    response = api_client.patch(f"/v1/users/{user.pk}/", {"first_name": "Jane"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_user(api_client, user_data):
    """Test user creation."""
    response = api_client.post("/v1/users/", user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username=user_data["username"]).exists()


@pytest.mark.django_db
def test_get_stts(api_client, user, stts):
    """Test STT view."""
    api_client.login(username=user.username, password="test_password")
    response = api_client.get("/v1/stts/all")
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["id"] == 1
    assert response.data[0]["stts"][0]["name"] == "Connecticut"
    assert response.data[-1]["id"] == 1000
    assert response.data[-1]["stts"][0]["name"] == "I work at OFA"


@pytest.mark.django_db
@pytest.mark.parametrize("role", User.Role.choices)
def test_set_profile_data(api_client, user, stts, role):
    """Test profile data can be set."""
    role = role[0]
    api_client.login(username=user.username, password="test_password")
    stt_id = STT.objects.first().id
    response = api_client.post(
        "/v1/users/set_profile/",
        {
            "first_name": "Joe",
            "last_name": "Bloggs",
            "stt": stt_id,
            "requested_role": role,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "first_name": "Joe",
        "last_name": "Bloggs",
        "stt": stt_id,
        "requested_role": role,
    }
    user.refresh_from_db()
    assert user.first_name == "Joe"
    assert user.last_name == "Bloggs"
    assert user.stt_id == stt_id
    assert user.requested_role == role
    assert user.role is None


@pytest.mark.django_db
def test_set_profile_data_anonymous(api_client, user, stts):
    """Test can't set profile data if not logged in."""
    stt_id = STT.objects.first().id
    response = api_client.post(
        "/v1/users/set_profile/",
        {
            "first_name": "Joe",
            "last_name": "Bloggs",
            "stt": stt_id,
            "requested_role": User.Role.ADMIN,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_set_profile_bad_role(api_client, user, stts):
    """Test only correct role choices are accepted."""
    api_client.login(username=user.username, password="test_password")
    stt_id = STT.objects.first().id
    response = api_client.post(
        "/v1/users/set_profile/",
        {
            "first_name": "Joe",
            "last_name": "Bloggs",
            "stt": stt_id,
            "requested_role": "foo",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_set_profile_with_only_name(api_client, user, stts):
    """Test setting profile with partial data."""
    api_client.login(username=user.username, password="test_password")
    response = api_client.post(
        "/v1/users/set_profile/", {"first_name": "Joe", "last_name": "Bloggs"},
    )
    assert response.data == {
        "first_name": "Joe",
        "last_name": "Bloggs",
        "stt": None,
        "requested_role": None,
    }
    user.refresh_from_db()
    assert user.first_name == "Joe"
    assert user.last_name == "Bloggs"
