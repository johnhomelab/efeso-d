from django.shortcuts import render
from patients.models import Patient

def home(request):
    # MVP: contar todos os pacientes (mais tarde vamos filtrar por clinic/tenant)
    patients_count = Patient.objects.count()

    return render(request, "ui/home.html", {
        "patients_count": patients_count,
    })