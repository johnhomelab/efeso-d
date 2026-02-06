from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth import get_user_model
from core.models import Clinic
from io import StringIO
import os

class CreateInitialTenantTest(TestCase):
    def test_command_creates_clinic_and_superuser(self):
        # Ensure clean slate (TestCase does this, but being explicit)
        Clinic.objects.all().delete()
        get_user_model().objects.all().delete()

        out = StringIO()
        call_command('create_initial_tenant', stdout=out)

        self.assertTrue(Clinic.objects.filter(slug='default').exists())
        User = get_user_model()
        self.assertTrue(User.objects.filter(username='admin').exists())
        self.assertIn('Created initial clinic', out.getvalue())
        self.assertIn('Created superuser', out.getvalue())

    def test_command_idempotency(self):
        out = StringIO()
        call_command('create_initial_tenant', stdout=out)
        call_command('create_initial_tenant', stdout=out)

        self.assertEqual(Clinic.objects.count(), 1)
        User = get_user_model()
        # Note: If tests run in parallel or share DB state, we might have issues, but TestCase isolates.
        # But we create 1 user.
        self.assertEqual(User.objects.count(), 1)
