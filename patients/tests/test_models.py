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
        self.assertEqual(patient.cpf, self.valid_cpf)

    def test_cpf_uniqueness_per_clinic(self):
        """Should raise IntegrityError (or ValidationError) when creating a patient with a duplicate CPF in the same clinic."""
        Patient.objects.create(
            clinic=self.clinic_a,
            full_name="Patient 1",
            cpf=self.valid_cpf
        )

        # Depending on how the constraint is enforced (DB vs App), it might raise IntegrityError
        with self.assertRaises(IntegrityError):
            Patient.objects.create(
                clinic=self.clinic_a,
                full_name="Patient 2",
                cpf=self.valid_cpf
            )

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
        self.assertEqual(patient_b.cpf, self.valid_cpf)

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
