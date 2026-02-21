from django.db import models


class Patient(models.Model):
    patient_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255, db_index=True)
    mobile = models.CharField(max_length=20, db_index=True)
    email = models.EmailField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    first_visit_date = models.DateField(null=True, blank=True)
    last_visit_date = models.DateField(null=True, blank=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_pending = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Appointment(models.Model):
    STATUS_SCHEDULED = "scheduled"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"
    STATUS_NO_SHOW = "no_show"

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_NO_SHOW, "No-show"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    scheduled_date = models.DateField(db_index=True)
    scheduled_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
    reason = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} on {self.scheduled_date}"


class Visit(models.Model):
    STATUS_PAID = "paid"
    STATUS_PARTIAL = "partial"
    STATUS_PENDING = "pending"

    STATUS_CHOICES = [
        (STATUS_PAID, "Paid"),
        (STATUS_PARTIAL, "Partial"),
        (STATUS_PENDING, "Pending"),
    ]

    PAYMENT_UPI = "upi"
    PAYMENT_CASH = "cash"
    PAYMENT_OTHER = "other"

    PAYMENT_CHOICES = [
        (PAYMENT_UPI, "UPI"),
        (PAYMENT_CASH, "Cash"),
        (PAYMENT_OTHER, "Other"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="visits")
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        related_name="visits",
        null=True,
        blank=True,
    )
    visit_date = models.DateField(db_index=True)
    symptoms = models.TextField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)
    visit_fee = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    next_appointment_date = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def balance(self):
        return (self.visit_fee or 0) - (self.amount_paid or 0)

    def __str__(self):
        return f"Visit {self.id} for {self.patient}"


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    google_drive_file_id = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    mime_type = models.CharField(max_length=100, null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class VisitExercise(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="visit_exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="visit_exercises")
    custom_instructions = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.exercise} for {self.visit}"


class ClinicSettings(models.Model):
    clinic_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255, null=True, blank=True)
    owner_email = models.EmailField()
    default_visit_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.clinic_name


class MonthlyReportLog(models.Model):
    STATUS_SENT = "sent"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_SENT, "Sent"),
        (STATUS_FAILED, "Failed"),
    ]

    year = models.IntegerField()
    month = models.IntegerField()
    generated_at = models.DateTimeField()
    sent_to = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Report {self.year}-{self.month} to {self.sent_to}"
