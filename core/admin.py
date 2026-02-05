from django.contrib import admin
from .models import Clinic


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "active", "created_at")
    list_filter = ("active",)
    search_fields = ("name", "slug")
    ordering = ("name",)
