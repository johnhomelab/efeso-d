
from django.db import models


class Clinic(models.Model):
    """
    Representa a clínica (tenant). Mesmo que você use só 1 agora,
    isso evita reescrita quando virar SaaS.
    """
    name = models.CharField("Nome da clínica", max_length=120)
    slug = models.SlugField("Slug", max_length=80, unique=True)

    active = models.BooleanField("Ativa", default=True)

    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Clínica"
        verbose_name_plural = "Clínicas"
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self) -> str:
        return self.name