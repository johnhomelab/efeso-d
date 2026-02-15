from django.test import TestCase
from django.core.management import call_command, CommandError
from django.contrib.auth import get_user_model
from core.models import Clinic
from io import StringIO
import os
from unittest.mock import patch

class CreateInitialTenantTest(TestCase):
    def setUp(self):
        Clinic.objects.all().delete()
        get_user_model().objects.all().delete()

    @patch.dict(os.environ, {"DJANGO_SUPERUSER_PASSWORD": "secure_password"})
    def test_command_creates_clinic_and_superuser(self):
        out = StringIO()
        call_command('create_initial_tenant', stdout=out)

        self.assertTrue(Clinic.objects.filter(slug='default').exists())
        User = get_user_model()
        self.assertTrue(User.objects.filter(username='admin').exists())
        self.assertIn('Created initial clinic', out.getvalue())
        self.assertIn('Created superuser', out.getvalue())

    @patch.dict(os.environ, {"DJANGO_SUPERUSER_PASSWORD": "secure_password"})
    def test_command_idempotency(self):
        out = StringIO()
        call_command('create_initial_tenant', stdout=out)
        call_command('create_initial_tenant', stdout=out)

        self.assertEqual(Clinic.objects.count(), 1)
        User = get_user_model()
        self.assertEqual(User.objects.count(), 1)

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_password_fails(self):
        # Remove password from env to trigger error
        if "DJANGO_SUPERUSER_PASSWORD" in os.environ:
             del os.environ["DJANGO_SUPERUSER_PASSWORD"]

        with self.assertRaises(CommandError) as cm:
            call_command('create_initial_tenant')
        self.assertIn("DJANGO_SUPERUSER_PASSWORD environment variable is missing", str(cm.exception))

    @patch.dict(os.environ, {"DJANGO_SUPERUSER_PASSWORD": "secure_password"})
    def test_existing_non_superuser_fails(self):
        # Create a regular user first
        User = get_user_model()
        User.objects.create_user(username="admin", email="admin@example.com", password="old_password")

        with self.assertRaises(CommandError) as cm:
             call_command('create_initial_tenant')
        self.assertIn("User 'admin' exists but is not a superuser", str(cm.exception))

class ClinicModelTest(TestCase):
    def test_clinic_str(self):
        """Test that the string representation of a Clinic is its name."""
        clinic = Clinic.objects.create(name="Test Clinic", slug="test-clinic")
        self.assertEqual(str(clinic), "Test Clinic")
