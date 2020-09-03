"""generate_test_users command."""

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db import IntegrityError, transaction

import factory

from ...models import STT


User = get_user_model()


def _get_random_stt():
    return STT.objects.order_by("?").first()


class Command(BaseCommand):
    """Command class."""

    help = "Generate a test user for each role."

    def handle(self, *args, **options):
        """Generate a test user for each role."""
        first_name = factory.Faker("first_name")
        last_name = factory.Faker("last_name")
        password = factory.Faker("password").generate()
        roles = [role_choice[0] for role_choice in User.Role.choices]
        roles.append(None)
        user_count = 0
        for role in roles:
            if role == User.Role.OFA_ANALYST:
                stt = STT.objects.get(id=-1)
            else:
                stt = _get_random_stt()
            if role is None:
                username = "test__unassigned"
            else:
                username = f"test__{role.replace(' ', '_').lower()}"
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=username,
                        email="test@example.com",
                        password=password,
                        first_name=first_name.generate(),
                        last_name=last_name.generate(),
                        role=role,
                        stt=stt,
                    )
            except IntegrityError:
                # User already exists.
                pass
            else:
                user_count += 1
                self.stdout.write(f"Username: {user.username}")
                self.stdout.write(f"Password: {password}")
                self.stdout.write()

        self.stdout.write(f"Created {user_count} users.")
