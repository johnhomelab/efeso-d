import os
from django.core.management.base import BaseCommand
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
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")

        if not User.objects.filter(username=username).exists():
            print(f"Creating superuser '{username}'...")
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f"Created superuser: {username}"))
        else:
            self.stdout.write(f"Superuser '{username}' already exists.")
