import re
from django.core.exceptions import ValidationError


def validate_cpf(value: str) -> None:
    """
    Valida CPF (Brasil). Aceita com ou sem máscara.
    - Permite vazio (para não obrigar o campo).
    - Rejeita CPFs com todos os dígitos iguais.
    - Valida dígitos verificadores.
    """
    if value is None:
        return

    cpf = re.sub(r"\D", "", value)

    # Se o campo estiver vazio, não valida (campo opcional)
    if cpf == "":
        return

    if len(cpf) != 11:
        raise ValidationError("CPF deve ter 11 dígitos.")

    if cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido.")

    # Calcula 1º dígito verificador
    sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dv1 = (sum1 * 10) % 11
    dv1 = 0 if dv1 == 10 else dv1

    # Calcula 2º dígito verificador
    sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dv2 = (sum2 * 10) % 11
    dv2 = 0 if dv2 == 10 else dv2

    if dv1 != int(cpf[9]) or dv2 != int(cpf[10]):
        raise ValidationError("CPF inválido.")