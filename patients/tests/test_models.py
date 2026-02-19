from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from core.models import Clinic
from patients.models import Patient

class PatientModelTest(TestCase):
    def setUp(self):
        # Create two clinics for tenancy testing
        self.clinic_a = Clinic.objects.create(name="Clinic A", slug="clinic-a")
        self.clinic_b = Clinic.objects.create(name="Clinic B", slug="clinic-b")

        # Valid CPF for testing
        self.valid_cpf = "111.444.777-35"

    def test_create_valid_patient(self):
        """Should create a patient successfully with valid data."""
        patient = Patient.objects.create(
            clinic=self.clinic_a,
            full_name="John Doe",
            cpf=self.valid_cpf
        )
        self.assertEqual(patient.full_name, "John Doe")
        self.assertEqual(patient.clinic, self.clinic_a)
        # Note: In safe mode, we expect normalization to happen if not conflicting
        self.assertEqual(patient.cpf, "11144477735")

    def test_cpf_uniqueness_per_clinic(self):
        """Should raise ValidationError on clean(), but handle duplicate gracefully on save() to avoid crash."""
        Patient.objects.create(
            clinic=self.clinic_a,
            full_name="Patient 1",
            cpf=self.valid_cpf
        )

        # 1. Test clean() raises ValidationError
        p2_clean = Patient(
            clinic=self.clinic_a,
            full_name="Patient 2 Clean",
            cpf=self.valid_cpf
        )
        with self.assertRaises(ValidationError):
            p2_clean.clean()

        # 2. Test save() handles collision gracefully (Safe Normalization)
        # It should detect the collision with the normalized value of Patient 1
        # and choose to save the raw value instead of crashing.
        p2_save = Patient(
            clinic=self.clinic_a,
            full_name="Patient 2 Save",
            cpf=self.valid_cpf
        )
        try:
            p2_save.save()
        except IntegrityError:
            self.fail("save() raised IntegrityError unexpectedly (should have skipped normalization)")

        # Verify it stored unnormalized because normalization was skipped due to collision
        p2_save.refresh_from_db()
        self.assertEqual(p2_save.cpf, self.valid_cpf)

    def test_cpf_uniqueness_cross_clinic(self):
        """Should allow the same CPF in different clinics."""
        Patient.objects.create(
            clinic=self.clinic_a,
            full_name="Patient A",
            cpf=self.valid_cpf
        )

        # Should succeed without error
        patient_b = Patient.objects.create(
            clinic=self.clinic_b,
            full_name="Patient B",
            cpf=self.valid_cpf
        )

        self.assertEqual(patient_b.clinic, self.clinic_b)
        # Normalized because no conflict in Clinic B
        self.assertEqual(patient_b.cpf, "11144477735")

    def test_invalid_cpf_validation(self):
        """Should raise ValidationError on full_clean() with invalid CPF."""
        invalid_cpf = "123.456.789-00" # Invalid check digits
        patient = Patient(
            clinic=self.clinic_a,
            full_name="Invalid CPF Patient",
            cpf=invalid_cpf
        )

        with self.assertRaises(ValidationError) as cm:
            patient.full_clean()

        self.assertIn('cpf', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['cpf'][0], "CPF inválido.")

    # --- New Tests added during merge ---

    def test_cpf_normalization_save(self):
        """Values should be normalized (digits only) when saving."""
        p = Patient(
            clinic=self.clinic_a,
            full_name="John Doe Norm",
            cpf="123.456.789-09"
        )
        p.save()
        p.refresh_from_db()
        self.assertEqual(p.cpf, "12345678909")

    def test_legacy_data_safe_normalization_explicit(self):
        """
        Explicit test for legacy data scenario.
        If a duplicate exists (legacy data), save() should NOT crash
        and should keep the mask (or original value).
        """
        # Create a "normalized" record
        Patient.objects.create(
            clinic=self.clinic_a,
            full_name="John Doe",
            cpf="12345678909"
        )

        # Create a second record that collides
        p2 = Patient(
            clinic=self.clinic_a,
            full_name="Jane Doe",
            cpf="123.456.789-09"
        )

        # Saving should NOT raise IntegrityError because logic in save() detects collision and keeps it as "123.456.789-09"
        try:
            p2.save()
        except IntegrityError:
            self.fail("Patient.save() raised IntegrityError on legacy duplicate scenario!")

        p2.refresh_from_db()
        # It should remain masked because normalization was skipped
        self.assertEqual(p2.cpf, "123.456.789-09")

    def test_blank_cpf_allowed(self):
        """Blank CPF should be allowed and not normalized to something else."""
        p = Patient.objects.create(
            clinic=self.clinic_a,
            full_name="No CPF",
            cpf=""
        )
        self.assertEqual(p.cpf, "")

        # Should allow multiple blank CPFs (unique constraint has condition)
        p2 = Patient.objects.create(
            clinic=self.clinic_a,
            full_name="No CPF 2",
            cpf=""
        )
        self.assertEqual(p2.cpf, "")
