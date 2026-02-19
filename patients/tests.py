from django.test import SimpleTestCase, TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from core.models import Clinic
from patients.models import Patient
from patients.validators import validate_cpf

class TestCPFValidator(SimpleTestCase):
    def test_valid_cpf_no_mask(self):
        """Should pass with a valid CPF without mask."""
        try:
            validate_cpf("12345678909")
            validate_cpf("11144477735")
        except ValidationError:
            self.fail("validate_cpf raised ValidationError unexpectedly!")

    def test_valid_cpf_with_mask(self):
        """Should pass with a valid CPF with mask."""
        try:
            validate_cpf("123.456.789-09")
            validate_cpf("111.444.777-35")
        except ValidationError:
            self.fail("validate_cpf raised ValidationError unexpectedly!")

    def test_none_value(self):
        """Should pass if value is None."""
        try:
            validate_cpf(None)
        except ValidationError:
            self.fail("validate_cpf raised ValidationError unexpectedly!")

    def test_empty_string(self):
        """Should pass if value is an empty string (stripped)."""
        try:
            validate_cpf("")
            validate_cpf("   ")
        except ValidationError:
            self.fail("validate_cpf raised ValidationError unexpectedly!")

    def test_invalid_length(self):
        """Should raise ValidationError if length is not 11 digits."""
        with self.assertRaises(ValidationError) as cm:
            validate_cpf("1234567890")
        self.assertEqual(cm.exception.message, "CPF deve ter 11 dígitos.")

        with self.assertRaises(ValidationError) as cm:
            validate_cpf("123456789012")
        self.assertEqual(cm.exception.message, "CPF deve ter 11 dígitos.")

    def test_all_digits_equal(self):
        """Should raise ValidationError if all digits are equal."""
        for i in range(10):
            cpf = str(i) * 11
            with self.assertRaisesRegex(ValidationError, "CPF inválido."):
                validate_cpf(cpf)

    def test_invalid_check_digits(self):
        """Should raise ValidationError if check digits are invalid."""
        # 123456789-09 is valid, so 123456789-00 should be invalid
        with self.assertRaisesRegex(ValidationError, "CPF inválido."):
            validate_cpf("12345678900")

        # 111444777-35 is valid, so 111444777-36 should be invalid
        with self.assertRaisesRegex(ValidationError, "CPF inválido."):
            validate_cpf("11144477736")

class TestPatientModel(TestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(name="Test Clinic", slug="test-clinic")

    def test_cpf_normalization_save(self):
        """Values should be normalized (digits only) when saving."""
        # 123.456.789-09 -> 12345678909 is a valid CPF for validate-docbr
        p = Patient(
            clinic=self.clinic,
            full_name="John Doe",
            cpf="123.456.789-09"
        )
        p.save()
        p.refresh_from_db()
        self.assertEqual(p.cpf, "12345678909")

    def test_cpf_uniqueness(self):
        """Uniqueness should be enforced on normalized values."""
        Patient.objects.create(
            clinic=self.clinic,
            full_name="John Doe",
            cpf="123.456.789-09"
        )

        # Second patient with same CPF digits, different format
        p2 = Patient(
            clinic=self.clinic,
            full_name="Jane Doe",
            cpf="12345678909"
        )
        with self.assertRaises(IntegrityError):
            p2.save()

    def test_blank_cpf_allowed(self):
        """Blank CPF should be allowed and not normalized to something else."""
        p = Patient.objects.create(
            clinic=self.clinic,
            full_name="No CPF",
            cpf=""
        )
        self.assertEqual(p.cpf, "")

        # Should allow multiple blank CPFs (unique constraint has condition)
        p2 = Patient.objects.create(
            clinic=self.clinic,
            full_name="No CPF 2",
            cpf=""
        )
        self.assertEqual(p2.cpf, "")
