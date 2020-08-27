"""Define custom authentication class."""

from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


User = get_user_model()


class CustomAuthentication(BaseAuthentication):
    """Define authentication and get user functions for custom authentication."""

    def authenticate(self, username=None):
        """Authenticate user with the request and username."""
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """Get user by the user id."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class LocalDevelopmentAuthentication(BaseAuthentication):
    """An authentication class that authenticates using a request header."""

    def authenticate(self, request):
        """Authenticate against request header."""
        username = request.headers.get("X-Username")
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such user")

        return (user, None)
