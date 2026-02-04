from django.db import models

class Paciente(models.Model):
    # --- OPÇÕES DE SELEÇÃO (Listas para os campos de escolha) ---
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    LEMBRETES_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('nao_enviar', 'Não enviar'),
    ]

    # --- DADOS PESSOAIS ---
    nome_completo = models.CharField(max_length=255)
    celular = models.CharField(max_length=20, help_text="Formato: +55 (DDD) 9...")
    telefone_fixo = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    lembretes_automaticos = models.CharField(
        max_length=20, 
        choices=LEMBRETES_CHOICES, 
        default='whatsapp'
    )
    
    como_conheceu = models.CharField(max_length=100, blank=True, null=True)
    profissao = models.CharField(max_length=100, blank=True, null=True)
    genero = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    paciente_estrangeiro = models.BooleanField(default=False)
    
    data_nascimento = models.DateField(blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True, verbose_name="Adicionar observações")
    categoria = models.CharField(max_length=100, blank=True, null=True, help_text="Ex: Particular, Convênio, VIP")

    # --- CONTATO DE EMERGÊNCIA ---
    emergencia_nome = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nome (Emergência)")
    emergencia_telefone = models.CharField(max_length=20, blank=True, null=True)

    # --- ENDEREÇO ---
    cep = models.CharField(max_length=9, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endereço com número")
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True) # Ex: BA

    # --- RESPONSÁVEL (Para menores de idade) ---
    responsavel_nome = models.CharField(max_length=100, blank=True, null=True)
    responsavel_cpf = models.CharField(max_length=14, blank=True, null=True)
    responsavel_nascimento = models.DateField(blank=True, null=True)

    # --- DADOS DO CONVÊNIO ---
    convenio_nome = models.CharField(max_length=100, default='Particular')
    convenio_titular = models.CharField(max_length=100, blank=True, null=True)
    convenio_carteirinha = models.CharField(max_length=50, blank=True, null=True)
    convenio_cpf_responsavel = models.CharField(max_length=14, blank=True, null=True)

    # Campos automáticos do sistema (não aparecem no formulário)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_completo
