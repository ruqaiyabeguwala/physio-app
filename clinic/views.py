from datetime import date, timedelta

from django.db.models import DecimalField, F, Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

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
