
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.accounts.models import User, UserRole


class Command(BaseCommand):
    help = "Seed mandatory initial user accounts."

    INITIAL_USERS = [
        {
            "name": "Administrator",
            "email": "admin@test.com",
            "password": "password123",
            "role": UserRole.ADMIN,
        },
        {
            "name": "User Satu",
            "email": "user1@test.com",
            "password": "password123",
            "role": UserRole.USER,
        },
        {
            "name": "User Dua",
            "email": "user2@test.com",
            "password": "password123",
            "role": UserRole.USER,
        },
    ]

    @transaction.atomic
    def handle(self, *args, **options):

        admin = None

        for user_data in self.INITIAL_USERS:

            email = user_data["email"]

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "name": user_data["name"],
                    "role": user_data["role"],
                    "created_by": admin,
                },
            )

            if created:
                user.set_password(user_data["password"])
                user.save(update_fields=["password"])

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created account: {email}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Account already exists: {email}"
                    )
                )

            # Administrator menjadi pembuat akun User.
            if user_data["role"] == UserRole.ADMIN:
                admin = user

        self.stdout.write(
            self.style.SUCCESS(
                "Initial user seeding completed successfully."
            )
        )
