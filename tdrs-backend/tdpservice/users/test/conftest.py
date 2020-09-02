"""User fixtures."""

import uuid

from django.core.management import call_command

import pytest


@pytest.fixture
def user_data():
    """Return user creation data."""
    return {
        "id": uuid.uuid4(),
        "username": "jsmith",
        "first_name": "John",
        "last_name": "Smith",
        "password": "correcthorsebatterystaple",
        "auth_token": "xxx",
    }


@pytest.fixture
def stts():
    """Populate STTs."""
    call_command("populate_stts")
