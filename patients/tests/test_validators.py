from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
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
