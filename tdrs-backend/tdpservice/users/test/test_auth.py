"""Test the custom authorization class."""
import os
import uuid

import pytest
from rest_framework import status

from ..authentication import CustomAuthentication
from ..api.utils import (
    generate_client_assertion,
    generate_jwt_from_jwks,
    generate_token_endpoint_parameters,
    response_internal,
    validate_nonce_and_state,
)


test_private_key = """
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
"""


class MockRequest:
    """Mock request class."""

    def __init__(self, status_code=status.HTTP_200_OK, data=None):
        self.status_code = status_code
        self.data = data

    def json(self):
        """Return data."""
        return self.data


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


def test_oidc_logout_with_token(api_client):
    """Test logging out with token redirects and token is removed."""
    session = api_client.session
    session["token"] = "abcd"
    session.save()
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


@pytest.mark.django_db
def test_response_internal(user):
    """Test response internal works."""
    response = response_internal(
        user, status_message="hello", id_token={"fake": "stuff"}
    )
    assert response.status_code == status.HTTP_200_OK


def test_generate_jwt_from_jwks(mocker):
    """Test JWT generation."""
    mock_get = mocker.patch("requests.get")
    jwk = {
        "kty": "EC",
        "crv": "P-256",
        "x": "f83OJ3D2xF1Bg8vub9tLe1gHMzV76e8Tus9uPHvRVEU",
        "y": "x_FEzRu9m36HLN_tue659LNpXW6pCyStikYjKIWI5a0",
        "kid": "Public key used in JWS spec Appendix A.3 example",
    }
    mock_get.return_value = MockRequest(data={"keys": [jwk]})
    assert generate_jwt_from_jwks() is not None


def test_validate_nonce_and_state():
    """Test nonece and state validation."""
    assert validate_nonce_and_state("x", "y", "x", "y") is True
    assert validate_nonce_and_state("x", "z", "x", "y") is False
    assert validate_nonce_and_state("x", "y", "y", "x") is False
    assert validate_nonce_and_state("x", "z", "y", "y") is False


def test_generate_client_assertion():
    """Test client assertion generation."""
    os.environ["JWT_KEY"] = test_private_key
    assert generate_client_assertion() is not None


def test_generate_token_endpoint_parameters():
    """Test token endpoint parameter generation."""
    os.environ["JWT_KEY"] = test_private_key
    params = generate_token_endpoint_parameters("test_code")
    assert "client_assertion" in params
    assert "client_assertion_type" in params
    assert "code=test_code" in params
    assert "grant_type=authorization_code" in params
