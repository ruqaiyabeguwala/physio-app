from datetime import date, timedelta
import csv

from django.db.models import DecimalField, F, Sum, Q
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django import forms

from .models import Patient, Visit

from .models import Visit


def _get_date_range(range_key: str):
    today = timezone.localdate()
    if range_key == "week":
        start = today - timedelta(days=6)
        end = today
    elif range_key == "month":
        start = today.replace(day=1)
        end = today
    elif range_key == "year":
        start = date(today.year, 1, 1)
        end = today
    else:
        range_key = "today"
        start = today
        end = today
    return range_key, start, end


def dashboard(request):
    range_key = request.GET.get("range", "today")
    range_key, start_date, end_date = _get_date_range(range_key)

    visits_qs = Visit.objects.filter(is_deleted=False, visit_date__range=(start_date, end_date))

    total_revenue = visits_qs.aggregate(
        total=Coalesce(
            Sum("amount_paid", output_field=DecimalField(max_digits=10, decimal_places=2)),
            0,
            output_field=DecimalField(max_digits=10, decimal_places=2),
        ),
    )["total"]

    visits_count = visits_qs.count()
    patients_count = visits_qs.values("patient_id").distinct().count()

    pending_qs = Visit.objects.filter(is_deleted=False).exclude(payment_status=Visit.STATUS_PAID)
    balance_expr = F("visit_fee") - F("amount_paid")
    pending_total = pending_qs.aggregate(
        total=Coalesce(
            Sum(balance_expr, output_field=DecimalField(max_digits=10, decimal_places=2)),
            0,
            output_field=DecimalField(max_digits=10, decimal_places=2),
        )
    )["total"]

    pending_list = (
        pending_qs.select_related("patient")
        .order_by("visit_date", "id")[:10]
    )

    revenue_by_date = (
        visits_qs.values("visit_date")
        .annotate(
            total=Coalesce(
                Sum("amount_paid", output_field=DecimalField(max_digits=10, decimal_places=2)),
                0,
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
        .order_by("visit_date")
    )

    recent_visits = (
        visits_qs.select_related("patient")
        .order_by("-visit_date", "-id")[:20]
    )

    context = {
        "range_key": range_key,
        "start_date": start_date,
        "end_date": end_date,
        "total_revenue": total_revenue,
        "pending_total": pending_total,
        "visits_count": visits_count,
        "patients_count": patients_count,
        "pending_list": pending_list,
        "revenue_by_date": revenue_by_date,
        "recent_visits": recent_visits,
    }
    return render(request, "dashboard.html", context)


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "full_name",
            "mobile",
            "email",
            "age",
            "gender",
            "address",
            "notes",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "mobile": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "gender": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }


def patients_list(request):
    query = request.GET.get("q", "").strip()
    patients = Patient.objects.all().order_by("full_name")
    if query:
        patients = patients.filter(Q(full_name__icontains=query) | Q(mobile__icontains=query))
    context = {
        "patients": patients,
        "query": query,
    }
    return render(request, "patients/list.html", context)


def patient_create(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect("patient_detail", pk=patient.pk)
    else:
        form = PatientForm()
    context = {
        "form": form,
        "is_edit": False,
    }
    return render(request, "patients/form.html", context)


def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    visits = patient.visits.filter(is_deleted=False).order_by("-visit_date", "-id")
    context = {
        "patient": patient,
        "visits": visits,
    }
    return render(request, "patients/detail.html", context)


def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("patient_detail", pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    context = {
        "form": form,
        "is_edit": True,
        "patient": patient,
    }
    return render(request, "patients/form.html", context)


def patients_export(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="patients.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "Patient ID",
            "Full name",
            "Mobile",
            "Email",
            "Age",
            "Gender",
            "Address",
            "First visit date",
            "Last visit date",
            "Total revenue",
            "Total pending",
        ]
    )
    for patient in Patient.objects.all().order_by("full_name"):
        writer.writerow(
            [
                patient.pk,
                patient.full_name,
                patient.mobile,
                patient.email,
                patient.age,
                patient.gender,
                patient.address,
                patient.first_visit_date,
                patient.last_visit_date,
                patient.total_revenue,
                patient.total_pending,
            ]
        )
    return response


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
