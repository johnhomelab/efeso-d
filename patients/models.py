from django.db import models
from core.models import Clinic

UF_CHOICES = [
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AP", "Amapá"),
    ("AM", "Amazonas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PR", "Paraná"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("SC", "Santa Catarina"),
    ("SP", "São Paulo"),
    ("SE", "Sergipe"),
    ("TO", "Tocantins"),
]


class Patient(models.Model):
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.PROTECT,
        related_name="patients",
        verbose_name="Clínica",
    )

    # Identificação
    full_name = models.CharField("Nome completo", max_length=150)
    gender = models.CharField(
        "Gênero",
        max_length=20,
        blank=True,
        choices=[
            ("male", "Masculino"),
            ("female", "Feminino"),
            ("other", "Outro"),
            ("na", "Prefiro não informar"),
        ],
    )
    birth_date = models.DateField("Data de nascimento", null=True, blank=True)

    # Contato
    whatsapp_phone = models.CharField("WhatsApp", max_length=20, blank=True)
    email = models.EmailField("Email", blank=True)
    extra_phone = models.CharField("Telefone extra", max_length=20, blank=True)

    # Dados gerais
    how_knew_clinic = models.CharField("Como conheceu a clínica", max_length=80, blank=True)
    profession = models.CharField("Profissão", max_length=80, blank=True)
    is_foreigner = models.BooleanField("Paciente estrangeiro", default=False)

    # Documentos
    cpf = models.CharField("CPF", max_length=14, blank=True)
    rg = models.CharField("RG", max_length=20, blank=True)

    # Observações / categorias
    notes = models.TextField("Observações", blank=True)
    categories = models.CharField("Categorias", max_length=200, blank=True)

    # Contato de emergência
    emergency_contact_name = models.CharField("Nome (emergência)", max_length=120, blank=True)
    emergency_contact_phone = models.CharField("Telefone (emergência)", max_length=20, blank=True)

    # Endereço
    cep = models.CharField("CEP", max_length=10, blank=True)
    address_line = models.CharField("Endereço", max_length=180, blank=True)
    address_number = models.CharField("Número", max_length=20, blank=True)
    address_complement = models.CharField("Complemento", max_length=80, blank=True)
    neighborhood = models.CharField("Bairro", max_length=80, blank=True)
    city = models.CharField("Cidade", max_length=80, blank=True)
    state = models.CharField("Estado", max_length=2, blank=True, 
choices=UF_CHOICES )

    # Responsável (para menores)
    guardian_name = models.CharField("Nome do responsável", max_length=150, blank=True)
    guardian_cpf = models.CharField("CPF do responsável", max_length=14, blank=True)
    guardian_birth_date = models.DateField("Nascimento do responsável", null=True, blank=True)

    # Convênio
    insurance_name = models.CharField("Convênio", max_length=120, blank=True, default="Particular")
    insurance_holder_name = models.CharField("Titular do convênio", max_length=150, blank=True)
    insurance_card_number = models.CharField("Número da carteirinha", max_length=50, blank=True)
    insurance_guardian_cpf = models.CharField("CPF do responsável (convênio)", max_length=14, blank=True)

    # Auditoria simples
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ["full_name"]
        indexes = [
            models.Index(fields=["clinic", "full_name"]),
            models.Index(fields=["clinic", "mobile_phone"]),
            models.Index(fields=["clinic", "cpf"]),
        ]
        constraints = [
            # CPF não pode ser "globalmente único" num SaaS.
            # Aqui garantimos unicidade por clínica, mas só quando CPF estiver preenchido.
            models.UniqueConstraint(
                fields=["clinic", "cpf"],
                name="uniq_patient_cpf_per_clinic",
                condition=~models.Q(cpf=""),
            )
        ]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.clinic})"