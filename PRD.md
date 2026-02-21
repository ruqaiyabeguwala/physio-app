Product Requirements Document (PRD)
===================================

Product: Physio Clinic Management MVP  
Owner: Physiotherapist-focused app  
Version: v1 (MVP)

1. Overview
-----------

- A lightweight web app for a single physiotherapy clinic.
- Focused on:
  - Managing patients and their visits.
  - Tracking appointments and follow-ups.
  - Tracking revenue and pending dues.
  - Sharing exercise content stored on Google Drive.
  - Sending visit summaries/exercise links via WhatsApp (manually) and monthly summaries via email.

2. Goals & Non-Goals
--------------------

### 2.1 Primary Goals

- Make day-to-day patient and visit management easy.
- Help the physio remember follow-ups and appointments.
- Give clear visibility into revenue and pending payments.
- Allow attaching exercise media from Google Drive without managing files in the app.
- Enable quick manual WhatsApp communication with patients.
- Provide monthly performance summary via email.

### 2.2 Non-Goals (Out of Scope for MVP)

- Advanced clinical tracking (pain scores, outcome scales, detailed medical history).
- Full EMR (electronic medical record) functionality.
- Online payment integration (Razorpay, Stripe, etc.).
- WhatsApp Business API automation (no automatic sending; only generate text and link).
- Multi-clinic support or multiple physio logins.
- Highly advanced analytics and custom reports.
- Role-based permissions (receptionist vs doctor).
- Complex notification automation (SMS, push notifications, etc.).

3. Target Users
---------------

### 3.1 Primary User

- Single physiotherapist (clinic owner) using the app themselves (desktop or mobile browser).

### 3.2 Future User (Not for MVP)

- Clinic assistant using the same account.

4. High-Level Scope
-------------------

The MVP includes:

- Patient management.
- Visit/session management.
- Appointment and follow-up management.
- Dashboard (revenue, attendance, dues).
- Exercise library integrated with Google Drive (service account + shared folder).
- Manual WhatsApp visit message generation.
- Monthly email report to clinic owner.
- Basic authentication and data export.

5. Functional Requirements
--------------------------

5.1 Patient Management
~~~~~~~~~~~~~~~~~~~~~~

**In scope**

- Create patient:
  - Fields:
    - Patient ID (auto-generated, unique).
    - Full name (required).
    - Mobile number (required; used for WhatsApp).
    - Email (optional).
    - Age (optional).
    - Gender (optional).
    - Address (optional, free text).
    - Notes/remarks (optional).
    - First visit date (auto-set when the first visit is created).
  - Behavior:
    - Duplicate detection: if the same mobile number already exists, app should show a warning and propose opening existing patient.

- View patient profile:
  - Shows:
    - Basic patient details.
    - Summary:
      - Total number of visits.
      - First visit date.
      - Last visit date.
      - Total revenue from this patient.
      - Total pending/overdue amount.
  - List of visits (most recent first):
    - Date.
    - Main reason/symptoms (short preview).
    - Payment status (Paid / Partial / Pending).

- Edit patient:
  - Allow editing all basic details (except Patient ID).
  - Changes should not break the link to existing visits.

- Search for patients:
  - Global search bar with:
    - Search by name (contains).
    - Search by phone number (exact match).
    - Search by patient ID (exact match).
  - Result list: name, phone, last visit date, pending amount (if any).

**Out of scope**

- Complex patient medical histories.
- Attachments directly to patients (files in DB).

5.2 Visit / Session Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**In scope**

- Create a visit for a patient:
  - Entry points:
    - From patient profile: "Add visit".
    - From today’s appointment: "Mark as arrived / Add visit".
  - Fields:
    - Visit ID (auto).
    - Patient ID (pre-filled).
    - Visit date (defaults to today; editable).
    - Symptoms/complaints (text).
    - Treatment/therapy given (text).
    - Payment:
      - Visit fee (amount owed for this session).
      - Amount paid.
      - Payment status (auto from amounts: Paid / Partial / Pending).
      - Payment method: UPI / Cash / Other.
      - Payment date (defaults to today; editable).
    - Notes/remarks (text).
    - Prescribed exercises (list of references to Exercise Library items; see 5.4).
    - Next appointment date (optional).
  - Behavior:
    - When creating a new visit for a patient who has any unpaid or partially paid previous visits, show at the top of the visit form:
      - The total outstanding amount from all previous visits.
      - A short breakdown listing the last unpaid/partially paid visits with their dates and balances.

- View visit details:
  - All fields above, including exercises (with links/thumbnails from Drive).

- Edit visit:
  - Allow correction of symptoms, treatment, payment, notes, and next appointment.

- Delete visit:
  - Simple "soft delete" is acceptable (e.g., mark inactive) for MVP; exact implementation can be internal.

**Out of scope**

- Clinical scoring (pain scales, questionnaires).
- Multiple types of visit billing (packages, plans, insurance).

5.3 Appointment & Follow-Up Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**In scope**

- Create appointment:
  - Fields:
    - Appointment ID (auto).
    - Patient (select existing or create new patient inline).
    - Date.
    - Time.
    - Reason/notes (optional).
    - Status: Scheduled / Completed / Cancelled / No-show.
  - Option to set this as "Next appointment" from a visit.

- View today’s appointments:
  - List view:
    - Time.
    - Patient name.
    - Reason.
    - Status.
  - Actions on each appointment:
    - "Mark as completed":
      - Optionally create a new visit for that patient (shortcut).
    - "Mark as no-show".
    - "Cancel" (with optional reason).

- Upcoming appointments:
  - Simple list for the next 7 days:
    - Date, time, patient, status.

- Linking appointments and visits:
  - When a visit is created from an appointment:
    - Visit should reference that appointment.
    - Appointment status auto-set to "Completed".

**Out of scope**

- Complex calendar integration (Google Calendar sync).
- Recurring appointments.

5.4 Exercise Library (Google Drive Integration)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**In scope**

- Exercise entity:
  - Fields:
    - Exercise ID (auto).
    - Name (e.g., "Shoulder pendulum").
    - Description/instructions (optional).
    - Category/body part (e.g., Shoulder, Knee, Back; free text or small fixed list).
    - Google Drive File ID.
    - File name (from Drive metadata).
    - File type (image/video, inferred from Drive).
    - Created at, updated at.

- Google Drive integration (service account + shared folder):
  - A service account is configured server-side.
  - One Google Drive folder (e.g., "Physio Exercises") is shared with the service account.
  - The app can:
    - List files from this shared folder (and optionally subfolders).
    - Read file metadata (name, MIME type, thumbnail link if available).
  - UI to "Import from Drive":
    - Screen showing list of files from that shared folder.
    - Physio can select one or more files to create Exercise entries.
    - On selection, the app creates Exercise records with the Drive metadata.

- Attaching exercises to visits:
  - On the visit form:
    - "Add exercises" button opens a searchable picker from the Exercise Library:
      - Filter by name and category.
    - Selected exercises are attached to the visit.
  - On visit view:
    - Show exercise list with:
      - Name.
      - Category.
      - "View" button:
        - Opens Google Drive viewer in a new tab using the file’s link.

- Exercise access model:
  - Assumption: exercises are generic (no patient faces), so links can use "Anyone with the link can view" or similar share setting.
  - App does not change Drive permissions; it assumes files in the shared folder are already configured appropriately.

**Out of scope**

- Uploading files directly to Drive from the app (for MVP; physio will upload via Drive UI).
- Per-patient private exercise media (no extra security model yet).
- Video streaming optimization or custom media players.

5.5 WhatsApp Message Generation (Manual Send)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**In scope**

- On visit creation or update:
  - Provide a "Generate WhatsApp message" action.
  - Auto-generate a message template including:
    - Patient name.
    - Visit date.
    - Treatment summary (short).
    - Payment amount and status.
    - Attached exercises (name + link to Drive).
  - Example structure:
    - "Dear [Name],
       Your physiotherapy session on [Date] is recorded.
       Treatment: [short text].
       Amount: ₹[amount], Status: [Paid/Pending].
       Exercises:
       1. [Exercise 1 name]: [link]
       2. [Exercise 2 name]: [link]
       Thank you."

- Manual send flow:
  - Two main actions:
    - "Copy message" button to copy text to clipboard.
    - "Open WhatsApp" button:
      - Opens wa.me or https://api.whatsapp.com/send URL with:
        - Patient’s phone number.
        - Pre-filled message text (URL-encoded).
  - User then sends the message manually inside WhatsApp.

**Out of scope**

- Automatic WhatsApp sending via WhatsApp Business API.
- Message status tracking (delivered/read).
- Message template management with approvals.

5.6 Dashboard & Reporting
~~~~~~~~~~~~~~~~~~~~~~~~~

**In scope**

- Main dashboard (home page):
  - Date filter presets: Today / This week / This month / This year.
  - Revenue summary:
    - Total revenue for selected period.
    - Optional pie or bar chart:
      - Revenue by day (for month view).
      - Or revenue by payment method (UPI vs cash) for the period.
  - Attendance:
    - Number of visits in selected period.
    - Number of unique patients in selected period.
    - List/table of today’s visits: patient name, time (if from appointment), payment status.
  - Pending dues:
    - Table of visits with status Partial/Pending.
    - Columns:
      - Patient name.
      - Visit date.
      - Amount owed.
      - Amount paid so far.
      - Balance.
    - Sort by oldest first.

- Monthly email report:
  - Automatically generated once per month (e.g., 1st of month for previous month) or triggered manually (implementation choice).
  - Recipient:
    - Clinic owner’s email (configured in settings).
  - Contents:
    - Period covered (e.g., "Report for January 2026").
    - Total revenue for the month.
    - Number of visits, number of unique patients.
    - Daily revenue breakdown (table).
    - Breakdown by payment method (UPI/Cash/Other).
    - List of pending dues at month-end (short table).
  - Format:
    - Simple HTML email with tables (no need for PDF in MVP).

**Out of scope**

- Custom report builders.
- Export to PDF for reports (beyond email itself).
- Complex multi-filter analytics (e.g., by diagnosis).

5.7 Authentication, Settings, and Data Export
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**In scope**

- Authentication:
  - Single-user app:
    - Simple email + password login (one account).
  - Session handling:
    - Basic session/cookie or token; user remains logged in until logout or timeout.

- Settings:
  - Clinic owner settings:
    - Name of clinic.
    - Owner name.
    - Owner email (used for reports).
    - Default visit fee (optional).
  - Integration settings:
    - Google Drive setup (internal, not necessarily exposed in UI for MVP if pre-configured).

- Data export:
  - Export patients to CSV.
  - Export visits to CSV.
  - Columns should cover key fields for external backup or spreadsheet use.

**Out of scope**

- Multi-user access control.
- Advanced security controls beyond reasonable best practices.

6. Non-Functional Requirements
------------------------------

- Performance:
  - Must handle a few thousand patients and tens of thousands of visits without noticeable lag in typical views (for a single clinic).
- Security:
  - Use standard practices to protect credentials and patient data.
  - Do not log sensitive data such as passwords.
- Reliability:
  - App should be stable for daily clinical use.
  - Data must not be lost on normal use flows.
- Usability:
  - Mobile-friendly layouts for core flows:
    - View today’s appointments.
    - Search patients.
    - Add visit.
    - Generate WhatsApp message.

7. Assumptions
--------------

- Single clinic, single physio user (one login).
- Physio is comfortable:
  - Uploading media directly to Google Drive.
  - Sharing one folder with a Google service account.
  - Manually sending WhatsApp messages (no automation required).
- Patients primarily use WhatsApp on their phones.
- Reports going to one fixed email address are sufficient.
