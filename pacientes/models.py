from django.db import models

class Paciente(models.Model):
    # Dados Básicos
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    telefone_whatsapp = models.CharField(max_length=20)
    
    # Prontuário focado em Implantodontia
    historico_medico = models.TextField(help_text="Alergias, diabetes, hipertensão")
    fumante = models.BooleanField(default=False)
    faz_uso_bifosfonatos = models.BooleanField(default=False, verbose_name="Uso de Bifosfonatos") # Crucial para implantes!
    
    # Campo para o Odontograma (armazenaremos os dados como JSON no futuro)
    mapa_bucal_json = models.JSONField(null=True, blank=True)
    
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo
