from datetime import date

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from .models import Patient, Visit


class SimpleLoginTests(TestCase):
    def test_redirects_to_login_when_not_authenticated(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("simple_login"), response["Location"])

    def test_login_with_valid_credentials_sets_session_and_redirects(self):
        response = self.client.post(
            reverse("simple_login"),
            {
                "username": settings.SIMPLE_LOGIN_USERNAME,
                "password": settings.SIMPLE_LOGIN_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))

        response2 = self.client.get(reverse("dashboard"))
        self.assertEqual(response2.status_code, 200)

    def test_logout_clears_session_and_redirects_to_login(self):
        self.client.post(
            reverse("simple_login"),
            {
                "username": settings.SIMPLE_LOGIN_USERNAME,
                "password": settings.SIMPLE_LOGIN_PASSWORD,
            },
        )
        response = self.client.get(reverse("simple_logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("simple_login"))

        response2 = self.client.get(reverse("dashboard"))
        self.assertEqual(response2.status_code, 302)
        self.assertIn(reverse("simple_login"), response2["Location"])


class VisitModelTests(TestCase):
    def test_balance_property_returns_fee_minus_paid(self):
        patient = Patient.objects.create(full_name="Test Patient", mobile="1234567890")
        visit = Visit.objects.create(
            patient=patient,
            visit_date=date.today(),
            visit_fee=Decimal("500.00"),
            amount_paid=Decimal("300.00"),
        )
        self.assertEqual(visit.balance, Decimal("200.00"))


class DashboardViewTests(TestCase):
    def test_dashboard_shows_visit_counts_and_totals(self):
        patient = Patient.objects.create(full_name="Dash Patient", mobile="9999999999")
        Visit.objects.create(
            patient=patient,
            visit_date=date.today(),
            visit_fee=Decimal("400.00"),
            amount_paid=Decimal("250.00"),
        )

        self.client.post(
            reverse("simple_login"),
            {
                "username": settings.SIMPLE_LOGIN_USERNAME,
                "password": settings.SIMPLE_LOGIN_PASSWORD,
            },
        )

        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_revenue", response.context)
        self.assertIn("visits_count", response.context)
        self.assertIn("patients_count", response.context)
        self.assertIn("pending_total", response.context)
        self.assertEqual(response.context["visits_count"], 1)
        self.assertEqual(response.context["patients_count"], 1)
        self.assertEqual(response.context["total_revenue"], Decimal("250.00"))
        self.assertEqual(response.context["pending_total"], Decimal("150.00"))


class PatientAndVisitViewTests(TestCase):
    def test_patient_create_creates_patient(self):
        self.client.post(
            reverse("simple_login"),
            {
                "username": settings.SIMPLE_LOGIN_USERNAME,
                "password": settings.SIMPLE_LOGIN_PASSWORD,
            },
        )

        response_get = self.client.get(reverse("patient_create"))
        self.assertEqual(response_get.status_code, 200)

        response_post = self.client.post(
            reverse("patient_create"),
            {
                "full_name": "Created Patient",
                "mobile": "1112223333",
                "email": "",
                "age": "",
                "gender": "",
                "address": "",
                "notes": "",
            },
        )
        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(Patient.objects.count(), 1)

    def test_visit_create_creates_visit_for_patient(self):
        self.client.post(
            reverse("simple_login"),
            {
                "username": settings.SIMPLE_LOGIN_USERNAME,
                "password": settings.SIMPLE_LOGIN_PASSWORD,
            },
        )

        patient = Patient.objects.create(full_name="Visit Patient", mobile="8887776666")

        response_get = self.client.get(reverse("visit_create"), {"patient": patient.pk})
        self.assertEqual(response_get.status_code, 200)

        response_post = self.client.post(
            reverse("visit_create") + f"?patient={patient.pk}",
            {
                "visit_date": date.today(),
                "symptoms": "",
                "treatment": "",
                "visit_fee": "600.00",
                "amount_paid": "400.00",
                "payment_method": "",
                "payment_date": "",
                "notes": "",
                "next_appointment_date": "",
            },
        )
        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(Visit.objects.count(), 1)
        visit = Visit.objects.first()
        self.assertEqual(visit.patient, patient)
        self.assertEqual(visit.visit_fee, Decimal("600.00"))
        self.assertEqual(visit.amount_paid, Decimal("400.00"))

    def test_patient_delete_without_visits_succeeds(self):
        self.client.post(
            reverse("simple_login"),
            {
                "username": settings.SIMPLE_LOGIN_USERNAME,
                "password": settings.SIMPLE_LOGIN_PASSWORD,
            },
        )

        patient = Patient.objects.create(full_name="No Visits Patient", mobile="5554443333")
        self.assertEqual(Patient.objects.count(), 1)

        response = self.client.post(reverse("patient_delete", args=[patient.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("patients_list"))
        self.assertEqual(Patient.objects.count(), 0)

    def test_patient_delete_with_visits_shows_error_and_keeps_patient(self):
        self.client.post(
            reverse("simple_login"),
            {
                "username": settings.SIMPLE_LOGIN_USERNAME,
                "password": settings.SIMPLE_LOGIN_PASSWORD,
            },
        )

        patient = Patient.objects.create(full_name="With Visits Patient", mobile="2223334444")
        Visit.objects.create(
            patient=patient,
            visit_date=date.today(),
            visit_fee=Decimal("200.00"),
            amount_paid=Decimal("0.00"),
        )
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Visit.objects.count(), 1)

        response = self.client.post(reverse("patient_delete", args=[patient.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("patients_list"))
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Visit.objects.count(), 1)
