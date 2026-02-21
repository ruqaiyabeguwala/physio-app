import csv
import os
from decimal import Decimal, InvalidOperation
from urllib.parse import quote
from datetime import date, timedelta
import re

from django.db.models import DecimalField, F, Sum, Q
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django import forms

from .models import Appointment, ClinicSettings, Exercise, Patient, Visit, VisitExercise

from .models import Visit

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except ImportError:
    service_account = None
    build = None


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

    today = timezone.localdate()
    visits_for_table = (
        visits_qs.select_related("patient")
        .order_by("visit_date", "id")
    )

    appointments_for_table = (
        Appointment.objects.select_related("patient")
        .filter(scheduled_date__range=(start_date, end_date))
        .order_by("scheduled_date", "scheduled_time", "id")
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
        "visits_for_table": visits_for_table,
        "appointments_for_table": appointments_for_table,
        "today": today,
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


def visits_export(request):
    range_key = request.GET.get("range", "today")
    range_key, start_date, end_date = _get_date_range(range_key)

    visits_qs = (
        Visit.objects.select_related("patient")
        .filter(is_deleted=False, visit_date__range=(start_date, end_date))
        .order_by("visit_date", "id")
    )

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename=\"visits.csv\"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "Visit ID",
            "Patient",
            "Mobile",
            "Visit date",
            "Visit fee",
            "Amount paid",
            "Amount due",
            "Payment status",
        ]
    )
    for visit in visits_qs:
        fee = visit.visit_fee or Decimal("0.00")
        paid = visit.amount_paid or Decimal("0.00")
        due = fee - paid
        writer.writerow(
            [
                visit.pk,
                visit.patient.full_name,
                visit.patient.mobile,
                visit.visit_date,
                fee,
                paid,
                due,
                visit.get_payment_status_display(),
            ]
        )
    return response


def visits_list(request):
    range_key = request.GET.get("range", "today")
    status_filter = request.GET.get("status", "all")
    sort_key = request.GET.get("sort", "date_desc")
    query = request.GET.get("q", "").strip()

    qs = Visit.objects.select_related("patient").filter(is_deleted=False)

    if range_key != "all":
        range_key, start_date, end_date = _get_date_range(range_key)
        qs = qs.filter(visit_date__range=(start_date, end_date))
    else:
        _, start_date, end_date = _get_date_range("today")

    if status_filter in {Visit.STATUS_PAID, Visit.STATUS_PARTIAL, Visit.STATUS_PENDING}:
        qs = qs.filter(payment_status=status_filter)

    if query:
        qs = qs.filter(
            Q(patient__full_name__icontains=query)
            | Q(patient__mobile__icontains=query)
        )

    qs = qs.annotate(due_amount=F("visit_fee") - F("amount_paid"))

    if sort_key == "date_asc":
        qs = qs.order_by("visit_date", "id")
    elif sort_key == "due_desc":
        qs = qs.order_by("-due_amount", "-visit_date", "-id")
    elif sort_key == "due_asc":
        qs = qs.order_by("due_amount", "-visit_date", "-id")
    else:
        sort_key = "date_desc"
        qs = qs.order_by("-visit_date", "-id")

    context = {
        "visits": qs,
        "range_key": range_key,
        "status_filter": status_filter,
        "sort_key": sort_key,
        "query": query,
        "start_date": start_date,
        "end_date": end_date,
    }
    return render(request, "visits/list.html", context)


class VisitForm(forms.ModelForm):
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all().order_by("name"),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
    )

    class Meta:
        model = Visit
        fields = [
            "visit_date",
            "symptoms",
            "treatment",
            "visit_fee",
            "amount_paid",
            "payment_method",
            "payment_date",
            "notes",
            "next_appointment_date",
        ]
        widgets = {
            "visit_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "symptoms": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "treatment": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "visit_fee": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "amount_paid": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
            "payment_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "next_appointment_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["exercises"].initial = self.instance.visit_exercises.values_list("exercise_id", flat=True)


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = [
            "name",
            "description",
            "category",
            "google_drive_file_id",
            "file_name",
            "mime_type",
            "thumbnail_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "google_drive_file_id": forms.HiddenInput(),
            "file_name": forms.HiddenInput(),
            "mime_type": forms.HiddenInput(),
            "thumbnail_url": forms.HiddenInput(),
        }


def _update_patient_summary(patient: Patient):
    visits = patient.visits.filter(is_deleted=False).order_by("visit_date", "id")
    if visits.exists():
        first = visits.first()
        last = visits.last()
        patient.first_visit_date = first.visit_date
        patient.last_visit_date = last.visit_date
        totals = visits.aggregate(
            total_revenue=Coalesce(
                Sum("amount_paid", output_field=DecimalField(max_digits=10, decimal_places=2)),
                0,
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
            total_pending=Coalesce(
                Sum(
                    F("visit_fee") - F("amount_paid"),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                ),
                0,
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
        )
        patient.total_revenue = totals["total_revenue"]
        patient.total_pending = totals["total_pending"]
    else:
        patient.first_visit_date = None
        patient.last_visit_date = None
        patient.total_revenue = Decimal("0.00")
        patient.total_pending = Decimal("0.00")
    patient.save(update_fields=["first_visit_date", "last_visit_date", "total_revenue", "total_pending"])


def _set_payment_status(visit: Visit):
    fee = visit.visit_fee or Decimal("0.00")
    paid = visit.amount_paid or Decimal("0.00")
    if paid >= fee and fee > 0:
        visit.payment_status = Visit.STATUS_PAID
    elif paid > 0:
        visit.payment_status = Visit.STATUS_PARTIAL
    else:
        visit.payment_status = Visit.STATUS_PENDING


def _format_whatsapp_number(raw: str):
    if not raw:
        return None
    digits = re.sub(r"\D", "", raw)
    if not digits:
        return None
    if len(digits) == 10:
        digits = "91" + digits
    if len(digits) < 10:
        return None
    return digits


def _get_drive_service():
    if not service_account or not build:
        return None
    key_file = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")
    if not key_file:
        return None
    scopes = ["https://www.googleapis.com/auth/drive.readonly"]
    try:
        creds = service_account.Credentials.from_service_account_file(key_file, scopes=scopes)
    except Exception:
        return None
    try:
        return build("drive", "v3", credentials=creds, cache_discovery=False)
    except Exception:
        return None


def _list_drive_media_files():
    service = _get_drive_service()
    folder_id = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")
    if not service or not folder_id:
        return [], "Google Drive is not configured"
    try:
        query = f"'{folder_id}' in parents and trashed=false"
        results = (
            service.files()
            .list(
                q=query,
                fields="files(id,name,mimeType,thumbnailLink)",
                pageSize=50,
            )
            .execute()
        )
        files = results.get("files", [])
        data = []
        for f in files:
            data.append(
                {
                    "id": f.get("id"),
                    "name": f.get("name"),
                    "mimeType": f.get("mimeType"),
                    "thumbnailLink": f.get("thumbnailLink"),
                }
            )
        return data, None
    except Exception:
        return [], "Error fetching files from Google Drive"


def visit_create(request):
    patient = None
    appointment = None
    patient_id = request.GET.get("patient")
    appointment_id = request.GET.get("appointment")
    if appointment_id:
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        patient = appointment.patient
    elif patient_id:
        patient = get_object_or_404(Patient, pk=patient_id)

    today = timezone.localdate()

    previous_unpaid = None
    previous_unpaid_total = Decimal("0.00")
    if patient:
        previous_unpaid = (
            patient.visits.filter(is_deleted=False)
            .exclude(payment_status=Visit.STATUS_PAID)
            .order_by("visit_date", "id")
        )
        for v in previous_unpaid:
            previous_unpaid_total += (v.visit_fee or Decimal("0.00")) - (v.amount_paid or Decimal("0.00"))

    if request.method == "POST" and request.POST.get("clear_dues") == "1":
        if not patient:
            patient = get_object_or_404(Patient, pk=request.POST.get("patient_id"))

        try:
            clear_amount = Decimal(request.POST.get("clear_amount") or "0")
        except (TypeError, InvalidOperation):
            clear_amount = Decimal("0.00")

        if clear_amount > 0:
            remaining = clear_amount
            outstanding_qs = (
                patient.visits.filter(is_deleted=False)
                .exclude(payment_status=Visit.STATUS_PAID)
                .order_by("visit_date", "id")
            )
            for old_visit in outstanding_qs:
                fee = old_visit.visit_fee or Decimal("0.00")
                paid = old_visit.amount_paid or Decimal("0.00")
                balance = fee - paid
                if balance <= 0 or remaining <= 0:
                    continue
                to_apply = min(balance, remaining)
                old_visit.amount_paid = paid + to_apply
                _set_payment_status(old_visit)
                if not old_visit.payment_date:
                    old_visit.payment_date = timezone.localdate()
                old_visit.save(update_fields=["amount_paid", "payment_status", "payment_date"])
                remaining -= to_apply

            _update_patient_summary(patient)

        previous_unpaid = (
            patient.visits.filter(is_deleted=False)
            .exclude(payment_status=Visit.STATUS_PAID)
            .order_by("visit_date", "id")
        )
        previous_unpaid_total = Decimal("0.00")
        for v in previous_unpaid:
            previous_unpaid_total += (v.visit_fee or Decimal("0.00")) - (v.amount_paid or Decimal("0.00"))

        form = VisitForm(initial={"visit_date": today, "payment_date": today})
    elif request.method == "POST":
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            if not patient:
                patient = get_object_or_404(Patient, pk=request.POST.get("patient_id"))
            visit.patient = patient
            if appointment:
                visit.appointment = appointment
            _set_payment_status(visit)
            visit.save()

            VisitExercise.objects.filter(visit=visit).delete()
            exercises_selected = form.cleaned_data.get("exercises")
            if exercises_selected:
                VisitExercise.objects.bulk_create(
                    [VisitExercise(visit=visit, exercise=ex) for ex in exercises_selected]
                )

            _update_patient_summary(patient)
            if appointment:
                appointment.status = Appointment.STATUS_COMPLETED
                appointment.save(update_fields=["status"])
            return redirect("visit_detail", pk=visit.pk)
    else:
        initial = {
            "visit_date": today,
            "payment_date": today,
        }
        form = VisitForm(initial=initial)

    context = {
        "form": form,
        "patient": patient,
        "appointment": appointment,
        "previous_unpaid": previous_unpaid,
        "previous_unpaid_total": previous_unpaid_total,
        "today": today,
    }
    return render(request, "visits/form.html", context)


def visit_detail(request, pk):
    visit = get_object_or_404(Visit.objects.select_related("patient", "appointment"), pk=pk, is_deleted=False)
    exercises = VisitExercise.objects.select_related("exercise").filter(visit=visit)
    clinic_name = "Hussain Physio"
    try:
        settings = ClinicSettings.objects.first()
        if settings and settings.clinic_name:
            clinic_name = settings.clinic_name
    except ClinicSettings.DoesNotExist:
        pass

    parts = [
        f"Visit summary for {visit.patient.full_name} at {clinic_name}",
        f"Date: {visit.visit_date}",
        f"Amount: ₹{visit.visit_fee} (Paid: ₹{visit.amount_paid}, Status: {visit.get_payment_status_display()})",
    ]
    if visit.symptoms:
        parts.append(f"Symptoms: {visit.symptoms}")
    if visit.treatment:
        parts.append(f"Treatment: {visit.treatment}")
    if exercises:
        exercise_names = ", ".join(e.exercise.name for e in exercises)
        parts.append(f"Exercises: {exercise_names}")
    message_text = "\n".join(parts)
    whatsapp_url = ""
    if visit.patient.mobile:
        phone = _format_whatsapp_number(visit.patient.mobile)
        if phone:
            whatsapp_url = f"https://wa.me/{phone}?text={quote(message_text)}"

    context = {
        "visit": visit,
        "exercises": exercises,
        "message_text": message_text,
        "whatsapp_url": whatsapp_url,
    }
    return render(request, "visits/detail.html", context)


def visit_clear_due(request, pk):
    visit = get_object_or_404(Visit.objects.select_related("patient"), pk=pk, is_deleted=False)
    if request.method == "POST":
        fee = visit.visit_fee or Decimal("0.00")
        paid = visit.amount_paid or Decimal("0.00")
        balance = fee - paid
        try:
            clear_amount = Decimal(request.POST.get("clear_amount") or "0")
        except (TypeError, InvalidOperation):
            clear_amount = Decimal("0.00")

        if balance > 0 and clear_amount > 0:
            to_apply = min(balance, clear_amount)
            visit.amount_paid = paid + to_apply
            _set_payment_status(visit)
            if not visit.payment_date:
                visit.payment_date = timezone.localdate()
            visit.save(update_fields=["amount_paid", "payment_status", "payment_date"])
            _update_patient_summary(visit.patient)
        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("patient_detail", pk=visit.patient.pk)
    return redirect("visit_detail", pk=visit.pk)


def visit_delete(request, pk):
    visit = get_object_or_404(Visit.objects.select_related("patient"), pk=pk, is_deleted=False)
    if request.method == "POST":
        visit.is_deleted = True
        visit.save(update_fields=["is_deleted"])
        _update_patient_summary(visit.patient)
        return redirect("visits_list")
    return redirect("visit_detail", pk=visit.pk)


def visit_edit(request, pk):
    visit = get_object_or_404(Visit, pk=pk, is_deleted=False)
    patient = visit.patient
    if request.method == "POST":
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            visit = form.save(commit=False)
            _set_payment_status(visit)
            visit.save()

            VisitExercise.objects.filter(visit=visit).delete()
            exercises_selected = form.cleaned_data.get("exercises")
            if exercises_selected:
                VisitExercise.objects.bulk_create(
                    [VisitExercise(visit=visit, exercise=ex) for ex in exercises_selected]
                )

            _update_patient_summary(patient)
            return redirect("visit_detail", pk=visit.pk)
    else:
        form = VisitForm(instance=visit)

    previous_unpaid = (
        patient.visits.filter(is_deleted=False)
        .exclude(payment_status=Visit.STATUS_PAID)
        .exclude(pk=visit.pk)
        .order_by("visit_date", "id")
    )

    context = {
        "form": form,
        "patient": patient,
        "appointment": visit.appointment,
        "previous_unpaid": previous_unpaid,
        "today": timezone.localdate(),
        "visit": visit,
    }
    return render(request, "visits/form.html", context)


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "patient",
            "scheduled_date",
            "scheduled_time",
            "reason",
            "notes",
        ]
        widgets = {
            "patient": forms.Select(attrs={"class": "form-select"}),
            "scheduled_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "scheduled_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "reason": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }


class SettingsForm(forms.ModelForm):
    class Meta:
        model = ClinicSettings
        fields = [
            "clinic_name",
            "owner_name",
            "owner_email",
            "default_visit_fee",
        ]
        widgets = {
            "clinic_name": forms.TextInput(attrs={"class": "form-control"}),
            "owner_name": forms.TextInput(attrs={"class": "form-control"}),
            "owner_email": forms.EmailInput(attrs={"class": "form-control"}),
            "default_visit_fee": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }


def appointments_list(request):
    today = timezone.localdate()
    base_qs = Appointment.objects.select_related("patient").order_by("scheduled_date", "scheduled_time", "id")
    today_appointments = base_qs.filter(scheduled_date=today)
    upcoming_appointments = base_qs.filter(scheduled_date__gt=today)
    past_appointments = base_qs.filter(scheduled_date__lt=today)
    context = {
        "today": today,
        "today_appointments": today_appointments,
        "upcoming_appointments": upcoming_appointments,
        "past_appointments": past_appointments,
    }
    return render(request, "appointments/list.html", context)


def appointment_create(request):
    initial = {
        "scheduled_date": timezone.localdate(),
    }
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = Appointment.STATUS_SCHEDULED
            appointment.save()
            return redirect("appointments_list")
    else:
        form = AppointmentForm(initial=initial)
    context = {
        "form": form,
    }
    return render(request, "appointments/form.html", context)


def appointment_complete(request, pk):
    appointment = get_object_or_404(Appointment.objects.select_related("patient"), pk=pk)
    if appointment.status == Appointment.STATUS_COMPLETED:
        return redirect("appointments_list")
    return redirect(f"{reverse('visit_create')}?appointment={appointment.pk}")


def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("appointments_list")
    else:
        form = AppointmentForm(instance=appointment)
    context = {"form": form}
    return render(request, "appointments/form.html", context)


def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appointment.delete()
        return redirect("appointments_list")
    return HttpResponseRedirect(reverse("appointments_list"))


def _import_exercises_stub():
    if Exercise.objects.exists():
        return 0
    samples = [
        {
            "name": "Shoulder pendulum",
            "description": "Gentle shoulder mobility exercise.",
            "category": "shoulder",
            "google_drive_file_id": "sample-shoulder-pendulum",
            "file_name": "Shoulder pendulum",
            "mime_type": "video/mp4",
        },
        {
            "name": "Knee extension",
            "description": "Seated knee extension strengthening.",
            "category": "knee",
            "google_drive_file_id": "sample-knee-extension",
            "file_name": "Knee extension",
            "mime_type": "video/mp4",
        },
        {
            "name": "Back bridge",
            "description": "Bridge exercise for lower back and glutes.",
            "category": "back",
            "google_drive_file_id": "sample-back-bridge",
            "file_name": "Back bridge",
            "mime_type": "video/mp4",
        },
    ]
    Exercise.objects.bulk_create(
        [
            Exercise(
                name=item["name"],
                description=item["description"],
                category=item["category"],
                google_drive_file_id=item["google_drive_file_id"],
                file_name=item["file_name"],
                mime_type=item["mime_type"],
            )
            for item in samples
        ]
    )
    return len(samples)


def exercises_list(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    exercises_qs = Exercise.objects.all().order_by("name")
    if query:
        exercises_qs = exercises_qs.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category:
        exercises_qs = exercises_qs.filter(category=category)

    categories = (
        Exercise.objects.exclude(category__isnull=True)
        .exclude(category__exact="")
        .order_by("category")
        .values_list("category", flat=True)
        .distinct()
    )

    context = {
        "exercises": exercises_qs,
        "query": query,
        "selected_category": category,
        "categories": categories,
    }
    return render(request, "exercises/list.html", context)


def exercises_drive_files(request):
    files, error = _list_drive_media_files()
    return JsonResponse({"files": files, "error": error})


def exercise_create(request):
    if request.method == "POST":
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save()
            return redirect("exercises_list")
    else:
        form = ExerciseForm()
    context = {
        "form": form,
    }
    return render(request, "exercises/form.html", context)


def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    return render(request, "exercises/detail.html", {"exercise": exercise})


def pending_payments(request):
    today = timezone.localdate()
    age_key = request.GET.get("age", "all")

    pending_qs = (
        Visit.objects.select_related("patient")
        .filter(is_deleted=False)
        .exclude(payment_status=Visit.STATUS_PAID)
    )

    if age_key in {"7", "30", "90"}:
        cutoff = today - timedelta(days=int(age_key))
        pending_qs = pending_qs.filter(visit_date__lte=cutoff)
    else:
        age_key = "all"

    balance_expr = F("visit_fee") - F("amount_paid")
    totals = pending_qs.aggregate(
        total_due=Coalesce(
            Sum(balance_expr, output_field=DecimalField(max_digits=10, decimal_places=2)),
            0,
            output_field=DecimalField(max_digits=10, decimal_places=2),
        )
    )

    pending_visits = pending_qs.order_by("visit_date", "id")

    context = {
        "pending_visits": pending_visits,
        "age_key": age_key,
        "today": today,
        "total_due": totals["total_due"],
    }
    return render(request, "pending_payments.html", context)


def pending_payments_export(request):
    today = timezone.localdate()
    age_key = request.GET.get("age", "all")

    pending_qs = (
        Visit.objects.select_related("patient")
        .filter(is_deleted=False)
        .exclude(payment_status=Visit.STATUS_PAID)
    )

    if age_key in {"7", "30", "90"}:
        cutoff = today - timedelta(days=int(age_key))
        pending_qs = pending_qs.filter(visit_date__lte=cutoff)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename=\"pending_payments.csv\"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "Visit ID",
            "Patient",
            "Mobile",
            "Visit date",
            "Visit fee",
            "Amount paid",
            "Amount due",
            "Payment status",
        ]
    )
    balance_expr = F("visit_fee") - F("amount_paid")
    for visit in pending_qs.order_by("visit_date", "id"):
        fee = visit.visit_fee or Decimal("0.00")
        paid = visit.amount_paid or Decimal("0.00")
        due = fee - paid
        writer.writerow(
            [
                visit.pk,
                visit.patient.full_name,
                visit.patient.mobile,
                visit.visit_date,
                fee,
                paid,
                due,
                visit.get_payment_status_display(),
            ]
        )
    return response


def settings_view(request):
    instance = ClinicSettings.objects.first()
    if request.method == "POST":
        form = SettingsForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("settings")
    else:
        form = SettingsForm(instance=instance)
    context = {
        "form": form,
    }
    return render(request, "settings.html", context)
