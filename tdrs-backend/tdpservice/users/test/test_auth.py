"""Test the custom authorization class."""
import uuid

import pytest
from rest_framework import status

from ..authentication import CustomAuthentication


@pytest.mark.django_db
def test_authentication(user):
    """Test authentication method."""
    auth = CustomAuthentication()
    authenticated_user = auth.authenticate(username=user.username)
    assert authenticated_user.username == user.username


@pytest.mark.django_db
def test_get_user(user):
    """Test get_user method."""
    auth = CustomAuthentication()
    found_user = auth.get_user(user.pk)
    assert found_user.username == user.username


@pytest.mark.django_db
def test_get_non_user(user):
    """Test that an invalid user does not return a user."""
    test_uuid = uuid.uuid1()
    auth = CustomAuthentication()
    nonuser = auth.get_user(test_uuid)
    assert nonuser is None


def test_oidc_auth(api_client):
    """Test login url redirects."""
    response = api_client.get("/v1/login/oidc")
    assert response.status_code == status.HTTP_302_FOUND


def test_oidc_logout(api_client):
    """Test logout url redirects."""
    response = api_client.get("/v1/logout/oidc")
    assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db
def test_logout(api_client, user):
    """Test logout."""
    api_client.login(username=user.username, password="test_password")
    response = api_client.get("/v1/logout")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_login_without_code(api_client):
    """Test login fails without code."""
    response = api_client.get("/v1/login")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"error": "OIDC Code not found!"}


@pytest.mark.django_db
def test_login_fails_without_state(api_client):
    """Test login fails without state."""
    response = api_client.get("/v1/login", {"code": "dummy"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"error": "OIDC State not found"}


@pytest.mark.django_db
def test_login_fails_with_bad_data(api_client):
    """Test login fails with bad data."""
    response = api_client.get("/v1/login", {"code": "dummy", "state": "dummy"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
