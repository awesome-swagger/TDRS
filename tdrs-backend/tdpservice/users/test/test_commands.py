"""Commands tests."""

from django.core.management import CommandError, call_command

import pytest

from ..models import Region, STT


@pytest.mark.django_db
def test_populating_regions_stts():
    """Test the command for populating regions and STTs."""
    call_command("populate_stts")
    assert Region.objects.filter(id=10).exists()
    assert STT.objects.filter(code="WA", type=STT.STTType.STATE).exists()
    assert STT.objects.filter(name="Puerto Rico", type=STT.STTType.TERRITORY).exists()
    assert STT.objects.filter(name="Chickasaw Nation", type=STT.STTType.TRIBE).exists()


@pytest.mark.django_db
def test_no_double_population(stts):
    """Test the population command raises an excepion if objects already exist."""
    with pytest.raises(CommandError):
        call_command("populate_stts")
