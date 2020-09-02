"""`populate_stts` command."""

import csv
from pathlib import Path

from django.core.management import BaseCommand, CommandError

from ...models import Region, STT


DATA_DIR = BASE_DIR = Path(__file__).resolve().parent / "data"


def _populate_regions():
    with open(DATA_DIR / "regions.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        regions = [Region(row["Id"]) for row in reader]
        Region.objects.bulk_create(regions)


def _get_states():
    with open(DATA_DIR / "states.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        return [
            STT(
                code=row["Code"],
                name=row["Name"],
                region_id=row["Region"],
                type=STT.STTType.STATE,
            )
            for row in reader
        ]


def _get_territories():
    with open(DATA_DIR / "territories.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        return [
            STT(
                code=row["Code"],
                name=row["Name"],
                region_id=row["Region"],
                type=STT.STTType.TERRITORY,
            )
            for row in reader
        ]


def _populate_tribes():
    with open(DATA_DIR / "tribes.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        stts = [
            STT(
                name=row["Name"],
                region_id=row["Region"],
                state=STT.objects.get(code=row["Code"]),
                type=STT.STTType.TRIBE,
            )
            for row in reader
        ]
        STT.objects.bulk_create(stts)


class Command(BaseCommand):
    """Command class."""

    help = "Populate regions, states, territories, and tribes."

    def handle(self, *args, **options):
        """Populate the various regions, states, territories, and tribes."""
        if Region.objects.exists() or STT.objects.exists():
            raise CommandError(
                "Database must be empty of regions or STTs to run this command."
            )
        _populate_regions()
        stts = _get_states()
        stts.extend(_get_territories())
        STT.objects.bulk_create(stts)
        _populate_tribes()
