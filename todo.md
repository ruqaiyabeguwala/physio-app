Build To-Do Plan for Physio Clinic App
======================================

How to Use This File
--------------------

- You do not need to remember prompts.
- Whenever you want to move forward, you can say:
  - “Use todo.md and execute Step X.”
- I will:
  - Read the step description here.
  - Follow exactly the actions defined for that step.
  - Ask you only if something is missing (e.g. password, specific environment detail).

Reset / Recovery Command
------------------------

- If at any point my answers look wrong, inconsistent with the MD files, or “hallucinated”, you can say:
  - “Reset using todo.md: re-read PRD.md, tech-stack.md, app-flow.md, front-end-guidelines.md, backend-guidelines.md, and todo.md, then re-execute Step X exactly as defined there.”
- When you say this, I will:
  - Ignore any previous assumptions and ad-hoc plans.
  - Re-sync only from the repository documents listed above.
  - Re-run the specified step (or steps) strictly according to todo.md and those docs.

Each step below includes:

- Goal: what we achieve in that step.
- Assistant actions: what I will do.
- What you will run locally: commands I’ll provide you to copy–paste in your terminal.
- Files that will be created/edited.

Step 1 – Environment and Tooling
--------------------------------

Goal:

- Have a working Python/Django environment on your machine using SQLite.

Assistant actions when you say “execute Step 1”:

- Check for:
  - Python version requirement (3.11+ recommended).
  - pip and virtual environment usage.
- Provide you with:
  - Exact commands to:
    - Create and activate a virtual environment in `/Users/ruqaiyabeguwala/Documents/projects/physio-app`.
    - Install Django and other base dependencies from tech-stack.md (Django, google-api-python-client placeholder, etc.).
  - Instructions to verify installation (e.g. `python -m django --version`).

What you will run:

- Terminal commands I provide, including:
  - `python -m venv venv` (or similar).
  - `source venv/bin/activate` (or similar on macOS).
  - `pip install django ...`.

Files touched:

- `requirements.txt` (or equivalent) created with core dependencies.

Step 2 – Django Project and App Skeleton
----------------------------------------

Goal:

- Create the Django project and main application according to tech-stack.md.

Assistant actions:

- Generate:
  - Commands to:
    - Run `django-admin startproject` in the `physio-app` folder.
    - Create a main app (e.g. `clinic`).
  - A proposal for project/app names.
- Provide the initial content or edits for:
  - `manage.py` (auto-generated, mainly referenced).
  - Project `settings.py`:
    - Configure SQLite.
    - Add main app to `INSTALLED_APPS`.
    - Static files settings.
  - Project `urls.py`:
    - Include main app URLs.
  - App `urls.py` skeleton.

What you will run:

- Commands I give, such as:
  - `django-admin startproject core .`
  - `python manage.py startapp clinic`
  - `python manage.py migrate`

Files touched:

- Django project files under `/Users/ruqaiyabeguwala/Documents/projects/physio-app`.

Step 3 – Backend Models and Database Schema
-------------------------------------------

Goal:

- Implement Django models matching backend-guidelines.md and run initial migrations.

Assistant actions:

- Translate backend-guidelines.md into Django models in `clinic/models.py`:
  - `Patient`
  - `Visit`
  - `Appointment`
  - `Exercise`
  - `VisitExercise`
  - `ClinicSettings`
  - `MonthlyReportLog` (optional)
- Ensure:
  - Field types and relationships match SQLite schema.
  - Helpful properties (e.g. `Visit.balance` property).
- Provide:
  - Commands to create migrations and apply them.

What you will run:

- `python manage.py makemigrations`
- `python manage.py migrate`

Files touched:

- `clinic/models.py`
- Migration files under `clinic/migrations/`.

Step 4 – URLs, Routing, and Base Template
-----------------------------------------

Goal:

- Define routes for each page and a base layout template with navigation.

Assistant actions:

- Using app-flow.md, define URL patterns for:
  - Dashboard (`/` or `/dashboard/`).
  - Patients list, new, details, edit.
  - Visits new, details, edit.
  - Appointments list, new.
  - Exercises list.
  - Pending payments.
  - Settings.
- Implement:
  - `clinic/urls.py` with all route definitions.
  - Update project `urls.py` to include `clinic/urls.py`.
- Create:
  - `templates/base.html` with:
    - Top navigation (Hussain Physio, Dashboard, Patients, Appointments, Exercises, Settings).
    - Content block for all pages.
    - Basic integration of Bootstrap CSS/JS plus the shared `static/css/main.css` theme so every page uses the same blue-and-white medical dashboard style.

What you will run:

- No special commands beyond re-running the dev server if needed.

Files touched:

- `core/urls.py` (or project-level URLs file).
- `clinic/urls.py`.
- `templates/base.html`.

Step 5 – Dashboard View and Template
------------------------------------

Goal:

- Implement the “Hussain Physio” dashboard as described in app-flow.md and front-end-guidelines.md.

Assistant actions:

- Implement in `clinic/views.py`:
  - A `dashboard` view that:
    - Reads the date filter (default Today).
    - Calculates:
      - Total revenue for selected period.
      - Pending amount (all time).
      - Visits and distinct patients for selected period.
    - Fetches:
      - Data for revenue over time (for the bar chart).
      - A list of pending payments (limited subset for the dashboard card).
      - A list of recent visits for the table.
- Create:
  - `templates/dashboard.html` implementing:
    - Header with date filter, "+ New visit", "More actions" dropdown.
    - Summary cards (revenue, pending, visits/patients).
    - Bar chart placeholder (`<canvas>`).
    - Pending payments card/table.
    - Visits table with Today/Month/Year filters and search box.
    - Use the shared `hp-card`, `hp-section`, and header classes so the layout matches other pages.
- Wire:
  - Dashboard URL to this view.

What you will run:

- `python manage.py runserver` to see the page in the browser.

Files touched:

- `clinic/views.py`.
- `templates/dashboard.html`.

Step 6 – Patients: List, Create, Detail, Edit, Export
-----------------------------------------------------

Goal:

- Build full patient management UI and backend.

Assistant actions:

- Implement views in `clinic/views.py`:
  - `patients_list`:
    - Supports search by name/phone.
    - Shows pending amount per patient (derived or cached).
    - Provides CSV export of all patients.
  - `patient_create`:
    - Shows new patient form.
    - On submit, creates patient and redirects to details.
  - `patient_detail`:
    - Shows summary card and visits list for that patient.
  - `patient_edit`:
    - Allows editing backend-guidelines.md fields.
- Create templates:
  - `templates/patients/list.html`
  - `templates/patients/form.html`
  - `templates/patients/detail.html`
  - All patient templates extend `base.html` and reuse the shared theme classes (`hp-card`, `hp-section`, header layout) for a consistent look.
- Add URLs:
  - `/patients/`, `/patients/new/`, `/patients/<id>/`, `/patients/<id>/edit/`, `/patients/export/`.

What you will run:

- Optionally tests or manual navigation:
  - Visit the Patients pages in the browser.

Files touched:

- `clinic/views.py`.
- `clinic/urls.py`.
- Templates under `templates/patients/`.

Step 7 – Visits: New, Follow-Up, Details, Edit, WhatsApp
--------------------------------------------------------

Goal:

- Implement full visit/session management, including dues banner and WhatsApp message generation.

Assistant actions:

- Implement views:
  - `visit_create`:
    - Accept optional patient or appointment as context.
    - Shows banner with pending dues from previous visits if any.
    - Saves new visit and updates patient summary fields.
  - `visit_detail`:
    - Shows visit data, payment info, exercises, and a “Generate Whatsapp Receipt” action.
  - `visit_edit`:
    - Allows editing visit fields.
- Implement WhatsApp:
  - In `visit_detail` template, add:
    - Bottom-of-page primary button “Generate Whatsapp Receipt” that opens a modal with the prefilled receipt text.
    - Button inside the modal that creates a `wa.me` link using patient mobile and prefilled text.
- Create templates:
  - `templates/visits/form.html`
  - `templates/visits/detail.html`
  - Visit templates also extend `base.html` and reuse the same header + card layout classes so the UI stays consistent with the dashboard and patients pages.
- Add URLs:
  - `/visits/new/`, `/visits/<id>/`, `/visits/<id>/edit/`.

What you will run:

- Manual checks in browser:
  - Create new visits.
  - Create follow-up visits via patient detail page.

Files touched:

- `clinic/views.py`.
- `clinic/urls.py`.
- Templates under `templates/visits/`.

Step 8 – Appointments: List, New, Complete
------------------------------------------

Goal:

- Provide appointment scheduling and completion flows.

Assistant actions:

- Implement views:
  - `appointments_list`:
    - Show today/upcoming/past appointments.
    - Provide actions to complete, cancel, or mark no-show.
  - `appointment_create`:
    - New appointment form.
  - `appointment_complete`:
    - Starts a new visit for that appointment (re-uses visit form).
- Templates:
  - `templates/appointments/list.html`
  - `templates/appointments/form.html`
- URLs:
  - `/appointments/`, `/appointments/new/`, `/appointments/<id>/complete/`.
- Ensure:
  - Completing an appointment creates a visit and updates `appointments.status`.

What you will run:

- Manual testing via the browser.

Files touched:

- `clinic/views.py`.
- `clinic/urls.py`.
- Templates under `templates/appointments/`.

Step 9 – Exercise Library and Visit–Exercise Linking
----------------------------------------------------

Goal:

- Implement the exercise library UI and link exercises to visits.

Assistant actions:

- Exercise list:
  - View: `exercises_list`:
    - Lists exercises with search and category filter.
  - Template: `templates/exercises/list.html`.
  - URL: `/exercises/`.
- Import from Google Drive:
  - Initially:
    - Implement a stub UI and backend that:
      - Assumes some exercise entries or uses a simple placeholder import function.
    - Later:
      - Use Google Drive API and service account to list files in the shared folder and create `Exercise` records.
- Visit–Exercise in visit form:
  - Modify visit form to:
    - Allow selecting exercises from the library (multi-select or a picker).
  - Implement linking using `VisitExercise` model.

What you will run:

- Manual checks:
  - Add exercises in DB (initially manually or via a simple form).
  - Attach exercises to visits and verify they show on visit details.

Files touched:

- `clinic/views.py`.
- `clinic/urls.py`.
- Templates under `templates/exercises/` and visit form.

Step 10 – Pending Payments Page and Settings
--------------------------------------------

Goal:

- Implement a dedicated pending payments page and a settings page for clinic configuration.

Assistant actions:

- Pending payments:
  - View: `pending_payments`:
    - Aggregates visits with `payment_status != 'paid'`.
    - Supports filters (e.g. age of dues).
    - Exports current view to CSV.
  - Template: `templates/pending_payments.html`.
  - URL: `/pending-payments/`.
- Settings:
  - View: `settings_view`:
    - Allows editing `ClinicSettings`.
  - Template: `templates/settings.html`.
  - URL: `/settings/`.

What you will run:

- Manual checks:
  - Open pending payments from dashboard card.
  - Edit settings and verify changes (e.g. clinic name, owner email).

Files touched:

- `clinic/views.py`.
- `clinic/urls.py`.
- Templates for pending payments and settings.

Step 11 – CSV Export Endpoints
------------------------------

Goal:

- Implement CSV exports for visits, patients, and pending payments as described in app-flow.md.

Assistant actions:

- Implement simple CSV views:
  - `export_patients_csv`.
  - `export_visits_csv` (respects current date filter).
  - `export_pending_payments_csv`.
- Add URLs:
  - `/patients/export/`, `/visits/export/`, `/pending-payments/export/`.
- Wire:
  - Export buttons on dashboard, Patients list, Pending payments page.

What you will run:

- Manual:
  - Trigger exports and open CSV files locally to verify fields.

Files touched:

- `clinic/views.py`.
- `clinic/urls.py`.

Step 12 – Monthly Report Email
------------------------------

Goal:

- Generate and send the monthly revenue/dues report via email.

Assistant actions:

- Implement:
  - Django management command (e.g. `send_monthly_report`) that:
    - Queries `Visit` for last month’s data.
    - Builds an HTML summary (revenue, visits, patients, pending dues).
    - Sends email using Django’s email backend to `ClinicSettings.owner_email`.
- Optionally:
  - Provide a view/action in Settings to trigger the report manually.
- Provide:
  - Email configuration snippet for settings (SMTP or other provider).

What you will run:

- `python manage.py send_monthly_report` (or similar).

Files touched:

- `clinic/management/commands/send_monthly_report.py`.
- `settings.py` email configuration.

Step 13 – Testing and Basic QA
------------------------------

Goal:

- Ensure the app works end-to-end and basic tests pass.

Assistant actions:

- Propose and implement:
  - A small set of Django tests:
    - Model tests (e.g. Visit balance, pending dues calculations).
    - Simple view tests (dashboard loads, patient create, visit create).
- Provide:
  - Commands to run tests: `python manage.py test`.
- Suggest:
  - Manual test checklist:
    - Create/edit patient.
    - Create visit and see dashboard update.
    - Create pending dues and see pending payments.
    - Attach exercises and generate WhatsApp message.

What you will run:

- `python manage.py test`.
- Manual navigation in browser.

Files touched:

- `clinic/tests.py` or tests package.
