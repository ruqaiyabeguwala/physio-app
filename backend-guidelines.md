Backend Guidelines (SQLite + Django)
====================================

Purpose
-------

- Define the backend data model and structure for the physio clinic app.
- Use SQLite as the main database with Django models on top.
- Support all features described in the PRD, tech stack, and app flow documents.

Overview
--------

- Backend framework:
  - Django (Python).
- Database:
  - SQLite (single file, always free, simple to manage).
- Auth:
  - Django’s built-in authentication system (single clinic owner user).
- Core data entities:
  - Patients.
  - Visits.
  - Appointments.
  - Exercises.
  - Visit–Exercise linking.
  - Clinic settings.
  - Optional monthly report logs.

Core Tables and Columns
-----------------------

Patients
~~~~~~~~

Table: `patients`

- `id` (INTEGER, primary key, auto-increment)
- `patient_code` (TEXT, unique, optional)
  - Human-friendly identifier (e.g. "P0001") that can be shown in UI.
- `full_name` (TEXT, required)
- `mobile` (TEXT, required, indexed)
- `email` (TEXT, nullable)
- `age` (INTEGER, nullable)
- `gender` (TEXT, nullable)
- `address` (TEXT, nullable)
- `notes` (TEXT, nullable)
- `first_visit_date` (DATE, nullable)
- `last_visit_date` (DATE, nullable)
- `total_revenue` (REAL, nullable, optional cached value)
- `total_pending` (REAL, nullable, optional cached value)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

Indexes:

- Index on `mobile`.
- Index on `full_name`.

Use cases:

- Search patients by name or mobile.
- Show summary stats per patient (visits, revenue, pending dues).

Visits
~~~~~~

Table: `visits`

- `id` (INTEGER, primary key, auto-increment)
- `patient_id` (INTEGER, foreign key → `patients.id`, indexed)
- `appointment_id` (INTEGER, foreign key → `appointments.id`, nullable)
- `visit_date` (DATE, required, indexed)
- `symptoms` (TEXT, nullable)
- `treatment` (TEXT, nullable)
- Payment fields:
  - `visit_fee` (REAL, required)
    - Total amount owed for this visit.
  - `amount_paid` (REAL, required, default 0)
  - `payment_status` (TEXT, required)
    - Expected values: `paid`, `partial`, `pending`.
  - `payment_method` (TEXT, nullable)
    - Expected values: `upi`, `cash`, `other` (or similar).
  - `payment_date` (DATE, nullable)
- `notes` (TEXT, nullable)
- `next_appointment_date` (DATE, nullable)
- `is_deleted` (BOOLEAN, default 0)  # for soft delete
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

Derived values (handled in code, not stored separately):

- `balance = visit_fee - amount_paid`.
- A patient’s total dues = sum of `balance` for all visits where `payment_status != 'paid'`.

Use cases:

- Create and manage visit entries (new and follow-up).
- Show pending dues banner based on previous visits for the same patient.
- Drive dashboard metrics:
  - Revenue by day/month/year.
  - Pending payments list.
  - Visits count.

Appointments
~~~~~~~~~~~~

Table: `appointments`

- `id` (INTEGER, primary key, auto-increment)
- `patient_id` (INTEGER, foreign key → `patients.id`, indexed)
- `scheduled_date` (DATE, required, indexed)
- `scheduled_time` (TIME, nullable, or use DATETIME in place of date + time)
- `status` (TEXT, required)
  - Expected values: `scheduled`, `completed`, `cancelled`, `no_show`.
- `reason` (TEXT, nullable)
- `notes` (TEXT, nullable)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

Relations and behavior:

- When a visit is created from an appointment:
  - `visits.appointment_id` is set.
  - `appointments.status` is updated to `completed`.

Use cases:

- Manage scheduled, upcoming, and past appointments.
- Support "Complete appointment" → "Create visit" flow.

Exercises (Google Drive Library)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Table: `exercises`

- `id` (INTEGER, primary key, auto-increment)
- `name` (TEXT, required)
- `description` (TEXT, nullable)
- `category` (TEXT, nullable)
  - Body part (e.g. `shoulder`, `knee`, `back`) or free text tag.
- `google_drive_file_id` (TEXT, required)
- `file_name` (TEXT, nullable)
- `mime_type` (TEXT, nullable)
- `thumbnail_url` (TEXT, nullable)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

Use cases:

- Store references to exercise media stored in Google Drive.
- Provide searchable library for visit forms.
- Enable linking exercises to visits and WhatsApp messages.

Visit–Exercise Linking
~~~~~~~~~~~~~~~~~~~~~~

Table: `visit_exercises`

- `id` (INTEGER, primary key, auto-increment)
- `visit_id` (INTEGER, foreign key → `visits.id`, indexed)
- `exercise_id` (INTEGER, foreign key → `exercises.id`, indexed)
- `custom_instructions` (TEXT, nullable)
  - Patient-specific variations (e.g. sets/reps/frequency).
- `created_at` (DATETIME)

Use cases:

- Attach multiple exercises to a visit.
- Show prescribed exercises on visit details.
- Include exercise links in WhatsApp messages and reports.

Clinic Settings
~~~~~~~~~~~~~~~

Table: `clinic_settings`

- `id` (INTEGER, primary key, auto-increment)
- `clinic_name` (TEXT, required)
- `owner_name` (TEXT, nullable)
- `owner_email` (TEXT, required)
  - Used for sending monthly reports.
- `default_visit_fee` (REAL, nullable)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

Notes:

- Typically only one row is used.
- Can be managed through a simple settings page.

Monthly Report Logs (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Table: `monthly_report_logs` (optional)

- `id` (INTEGER, primary key, auto-increment)
- `year` (INTEGER, required)
- `month` (INTEGER, required)
- `generated_at` (DATETIME, required)
- `sent_to` (TEXT, required)
- `status` (TEXT, required)
  - Expected values: `sent`, `failed`.
- `error_message` (TEXT, nullable)

Use cases:

- Keep track of when monthly reports were generated and sent.
- Help debug issues with report delivery.

Authentication
--------------

- Use Django’s built-in `User` model and related auth tables.
- Characteristics:
  - Single clinic owner account in MVP.
  - Username/email + password login.
  - All app routes require authentication.
- No custom tables required for auth in this MVP.

Indexes and Performance
-----------------------

- Suggested indexes for SQLite:
  - `patients(mobile)`
  - `patients(full_name)`
  - `visits(patient_id, visit_date)`
  - `visits(visit_date)`
  - `appointments(scheduled_date)`
  - `visit_exercises(visit_id)`
  - `visit_exercises(exercise_id)`
- This supports:
  - Fast patient lookup.
  - Efficient date-range queries for dashboard.
  - Quick joins between patients, visits, appointments, and exercises.

Key Backend Behaviors
---------------------

- On creating a new visit:
  - Update `patients.first_visit_date` if this is the first visit.
  - Update `patients.last_visit_date`.
  - Optionally recalculate `patients.total_revenue` and `patients.total_pending` or leave as derived.
- Pending dues banner for follow-up visits:
  - When opening the visit form for an existing patient:
    - Query all previous visits with `payment_status != 'paid'`.
    - Compute total outstanding balance.
    - Show total and a short list of recent unpaid/partial visits.
- Dashboard queries:
  - Revenue:
    - Sum of `amount_paid` from `visits` with `payment_status = 'paid'` in given date range.
  - Pending amount:
    - Sum of `visit_fee - amount_paid` where `payment_status != 'paid'` across all time.
  - Visits/Patients:
    - Count of visits and distinct patients in a date range.

Integration Points
------------------

- Google Drive:
  - Server-side code uses a Google service account and Drive API.
  - Imports file metadata into `exercises` table.
  - No binary files stored in the database.
- Email:
  - Use Django email utilities with SMTP or email provider.
  - Monthly reports aggregate data from `visits` and format as HTML.
- WhatsApp:
  - Backend assembles text for messages (patient, visit, exercises, payment).
  - Frontend uses `wa.me` / `api.whatsapp.com` links for manual sending.

Django Model Mapping (High-Level)
---------------------------------

Each table corresponds to a Django model:

- `Patient` → `patients`
- `Visit` → `visits`
- `Appointment` → `appointments`
- `Exercise` → `exercises`
- `VisitExercise` → `visit_exercises`
- `ClinicSettings` → `clinic_settings`
- `MonthlyReportLog` → `monthly_report_logs` (optional)

Models use:

- `ForeignKey` for relations (patient–visits, patient–appointments, visit–appointments, visit–exercises).
- `DateField`, `DateTimeField`, `FloatField` (or `DecimalField`) for amounts.
- `CharField`/`TextField` for text attributes.

