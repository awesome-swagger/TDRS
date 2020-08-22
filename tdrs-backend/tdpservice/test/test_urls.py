"""Test main routing works."""

from django.test import TestCase
from django.urls import reverse


class TestUrlResponses(TestCase):
    """Test url responses."""

    def test_oidc_auth(self):
        """Test login url redirects."""
        response = self.client.get(reverse("oidc-auth"))
        self.assertEqual(response.status_code, 302)

    def test_oidc_logout(self):
        """Test logout url redirects."""
        response = self.client.get(reverse("oidc-logout"))
        self.assertEqual(response.status_code, 302)
