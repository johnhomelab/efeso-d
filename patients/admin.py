
from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "clinic", "mobile_phone", "cpf", "created_at")
    list_filter = ("clinic", "gender")
    search_fields = ("full_name", "mobile_phone", "cpf", "email")
    ordering = ("full_name",)