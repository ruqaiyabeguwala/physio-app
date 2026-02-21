from django.http import HttpResponse
from django.shortcuts import render


def dashboard(request):
    return render(request, "dashboard.html")


def patients_list(request):
    return HttpResponse("Patients list")


def patient_create(request):
    return HttpResponse("New patient form")


def patient_detail(request, pk):
    return HttpResponse(f"Patient detail {pk}")


def patient_edit(request, pk):
    return HttpResponse(f"Edit patient {pk}")


def visit_create(request):
    return HttpResponse("New visit form")


def visit_detail(request, pk):
    return HttpResponse(f"Visit detail {pk}")


def visit_edit(request, pk):
    return HttpResponse(f"Edit visit {pk}")


def appointments_list(request):
    return HttpResponse("Appointments list")


def appointment_create(request):
    return HttpResponse("New appointment form")


def appointment_complete(request, pk):
    return HttpResponse(f"Complete appointment {pk}")


def exercises_list(request):
    return HttpResponse("Exercises list")


def pending_payments(request):
    return HttpResponse("Pending payments")


def settings_view(request):
    return HttpResponse("Settings")
