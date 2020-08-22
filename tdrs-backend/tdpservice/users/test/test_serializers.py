"""Test user serializers."""

from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict
from django.test import TestCase

from nose.tools import eq_, ok_

from ..serializers import CreateUserSerializer
from .factories import UserFactory


class TestCreateUserSerializer(TestCase):
    """Define methods for testing the user serializers."""

    def setUp(self):
        """Get test user for tests."""
        self.user_data = model_to_dict(UserFactory.build())

    def test_serializer_with_empty_data(self):
        """If an empty serialized request is returned it should not be valid."""
        serializer = CreateUserSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        """If a serializer has valid data it will return a valid object."""
        serializer = CreateUserSerializer(data=self.user_data)
        ok_(serializer.is_valid())

    def test_serializer_hashes_password(self):
        """The serializer should hash the user's password."""
        serializer = CreateUserSerializer(data=self.user_data)
        ok_(serializer.is_valid())

        user = serializer.save()
        ok_(check_password(self.user_data.get("password"), user.password))
