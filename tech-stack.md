Tech Stack for Physio Clinic Management MVP
===========================================

Overview
--------

- Goal: Build a lightweight, reliable, low-cost web app for a single physiotherapy clinic.
- Approach: Use a single Python-based web stack where backend and UI live together.
- Hosting: Single server or simple hosting; no separate frontend deployment.

Core Technologies
-----------------

- Backend and Web Framework:
  - Django (Python)
  - Responsibilities:
    - HTTP routing and views.
    - HTML rendering via Django templates.
    - Form handling and validation.
    - Authentication and sessions.
    - Integration with SQLite, Google Drive API, and email.

- Programming Language:
  - Python (3.11+ recommended)
  - Reasons:
    - Mature ecosystem for web apps and integrations.
    - Good support for SQLite, Google APIs, and email.

- Database:
  - SQLite
  - Usage:
    - Primary relational database for all app data:
      - Patients, Visits, Appointments, Exercises.
      - Authentication users and sessions (via Django auth).
    - Stored as a single file on the server.
  - Why:
    - Always free.
    - Extremely simple to set up (no separate DB server).
    - Easily handles the expected scale (tens of thousands of rows).

- Frontend/UI:
  - Django Templates (server-rendered HTML) extending a shared `base.html`.
  - CSS:
    - Bootstrap for layout and base components.
    - A single custom stylesheet `static/css/main.css` for:
      - Blue-and-white medical theme.
      - Card styles (`hp-card`, `hp-card-accent`).
      - Page layout helpers (`hp-section`, `hp-page-header`, etc.).
  - JavaScript:
    - Minimal custom JS for:
      - Form enhancements (date pickers, modals).
      - Dashboard charts (using a lightweight chart library such as Chart.js).
  - Why:
    - No separate frontend stack (React/Angular) to manage.
    - Fast to build form-heavy, table-heavy clinic flows with a consistent theme across all pages.

Integrations
------------

- Google Drive (Exercise Library):
  - Google Cloud Service Account:
    - Configured in Google Cloud Console.
    - Service account key stored securely on the server.
  - Shared Folder:
    - One Google Drive folder (e.g., "Physio Exercises") shared with the service account.
  - Google Drive API:
    - Used from Django views or background tasks to:
      - List files in the shared folder.
      - Read file metadata (name, mime type, thumbnail links).
    - App stores only:
      - File ID.
      - File name.
      - Type (image/video).
      - Category and description.

- Email (Monthly Reports):
  - Email Sending Library:
    - Django’s built-in email utilities.
    - Underlying SMTP provider:
      - Option 1: Clinic Gmail account (less ideal for production).
      - Option 2: Dedicated email service (Resend, SendGrid, etc.).
  - Usage:
    - Send monthly summary email to clinic owner.
    - Potential future use for appointment reminders.

- WhatsApp (Manual Message Flow):
  - No official API integration in MVP.
  - Approach:
    - Generate WhatsApp message text on the server or client.
    - Use wa.me or https://api.whatsapp.com/send links with:
      - Patient phone number.
      - URL-encoded message text.
    - User manually sends the message in WhatsApp.

Authentication and Security
---------------------------

- Authentication:
  - Django’s built-in authentication system.
  - Single clinic owner user account (email/username + password).
  - Session-based login with cookies.

- Authorization:
  - All application pages protected behind login.
  - No role-based permissions in MVP (only clinic owner).

- Security Practices:
  - Use HTTPS in production (via hosting provider or reverse proxy).
  - Keep service account keys and email credentials in environment variables.
  - Avoid logging sensitive patient or credential data.

Background and Scheduling
-------------------------

- Monthly Reports:
  - Approach:
    - Scheduled task that triggers a Django management command or HTTP endpoint.
    - Examples:
      - Cron job on the server.
      - Hosting provider scheduled task feature (if supported).
  - Task:
    - Aggregates monthly data from SQLite.
    - Sends email via configured SMTP.

Deployment
----------

- Environment:
  - Linux server or PaaS running on Google Cloud (e.g., a small Compute Engine VM, Cloud Run, or similar Google Cloud-hosted environment).
  - Components:
    - Django app (Gunicorn or similar WSGI server).
    - Reverse proxy (e.g., Nginx) or platform-provided HTTP proxy.

- Static Assets:
  - Serve CSS/JS via Django collectstatic and the web server or hosting platform.
  - For MVP scale, serving static files directly from the same server is acceptable.

Development Tooling
-------------------

- Package Management:
  - pip or pip-tools / Poetry (optional) to manage Python dependencies.

- Key Dependencies (Python):
  - Django.
  - google-api-python-client (or Google SDK) for Drive API.
  - django-environ or similar for environment variable management.

- Local Development:
  - Run Django’s development server.
  - Use the default SQLite database.
  - Use test Google Drive folder and test email configuration.

Future Evolution
----------------

- If the clinic grows or needs more users/branches:
  - Swap SQLite for PostgreSQL with minimal schema changes.
  - Introduce role-based access (clinic staff vs owner).
  - Optionally add a React or mobile client consuming Django as a pure API.
