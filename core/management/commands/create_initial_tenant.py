import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from core.models import Clinic

class Command(BaseCommand):
    help = "Creates an initial Clinic and Superuser if they do not exist. Useful for fresh deployments."

    def handle(self, *args, **options):
        self.stdout.write("Checking initial data...")

        # 1. Create Default Clinic
        clinic_slug = os.getenv("INITIAL_CLINIC_SLUG", "default")
        clinic_name = os.getenv("INITIAL_CLINIC_NAME", "Default Clinic")

        clinic, created = Clinic.objects.get_or_create(
            slug=clinic_slug,
            defaults={"name": clinic_name, "active": True}
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created initial clinic: {clinic.name} ({clinic.slug})"))
        else:
            self.stdout.write(f"Clinic '{clinic.slug}' already exists.")

        # 2. Create Superuser
        User = get_user_model()
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not password:
             raise CommandError("DJANGO_SUPERUSER_PASSWORD environment variable is missing. Cannot create superuser.")

        user = User.objects.filter(username=username).first()

        if not user:
            self.stdout.write(f"Creating superuser '{username}'...")
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f"Created superuser: {username}"))
        else:
            if user.is_superuser:
                self.stdout.write(f"Superuser '{username}' already exists.")
            else:
                 raise CommandError(f"User '{username}' exists but is not a superuser. Please fix manually.")
