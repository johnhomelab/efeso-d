import re
from django.core.exceptions import ValidationError
from validate_docbr import CPF


def validate_cpf(value: str) -> None:
    """
    Valida CPF (Brasil). Aceita com ou sem máscara.
    - Permite vazio (para não obrigar o campo).
    - Rejeita CPFs com todos os dígitos iguais.
    - Valida dígitos verificadores usando validate-docbr.
    """
    if value is None:
        return

    # Remove caracteres não numéricos
    cpf_digits = re.sub(r"\D", "", value)

    # Se o campo estiver vazio, não valida (campo opcional)
    if cpf_digits == "":
        return

    if len(cpf_digits) != 11:
        raise ValidationError("CPF deve ter 11 dígitos.")

    validator = CPF()
    # validate-docbr retorna True se for válido, False caso contrário
    if not validator.validate(cpf_digits):
        raise ValidationError("CPF inválido.")
