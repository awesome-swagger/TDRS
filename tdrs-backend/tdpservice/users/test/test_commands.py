"""Commands tests."""

from django.contrib.auth import get_user_model
from django.core.management import call_command

import pytest

from ..models import Region, STT


User = get_user_model()


@pytest.mark.django_db
def test_populating_regions_stts():
    """Test the command for populating regions and STTs."""
    call_command("populate_stts")
    assert Region.objects.filter(id=10).exists()
    assert STT.objects.filter(code="WA", type=STT.STTType.STATE).exists()
    assert STT.objects.filter(name="Puerto Rico", type=STT.STTType.TERRITORY).exists()
    assert STT.objects.filter(name="Chickasaw Nation", type=STT.STTType.TRIBE).exists()


@pytest.mark.django_db
def test_no_double_stt_population(stts):
    """Test the STT population command doesn't create extra objects."""
    original_stt_count = STT.objects.count()
    call_command("populate_stts")
    assert STT.objects.count() == original_stt_count


@pytest.mark.django_db
def test_generate_test_users(stts):
    """Test the command for generating test users."""
    call_command("generate_test_users")
    assert User.objects.count() == len(User.Role.choices) + 1


@pytest.mark.django_db
def test_no_double_user_generation(stts):
    """Test the user generation command doesn't create extra users."""
    call_command("generate_test_users")
    original_user_count = User.objects.count()
    call_command("generate_test_users")
    assert User.objects.count() == original_user_count
