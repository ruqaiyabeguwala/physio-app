App Flow and Frontend Guidelines
================================

Purpose
-------

- Define how a user moves through the app (screens and actions).
- Specify where and how data is entered, viewed, exported, and acted on.
- Keep the UI minimal, professional, and fast to use in a clinic.

Global UI Principles
--------------------

- Overall look:
  - Clean, minimal interface with a single primary blue accent.
  - Soft blue/white background, white cards, subtle shadows.
  - All pages use the same base layout (`base.html`) and theme from `static/css/main.css`.
- Typography:
  - One professional sans-serif (Inter, Roboto, or system).
  - Consistent sizes:
    - Page title: 20–24 px.
    - Section titles: 16–18 px.
    - Table text: 13–14 px.
  - Use semibold for titles and table headers.
- Colors:
  - Primary accent: calm blue/teal for buttons and highlights.
  - Status colors:
    - Paid = soft green.
    - Pending/partial = amber.
    - Overdue (older dues) = muted red.
- Components:
  - Use consistent cards for the main blocks (summary, charts, tables, forms) using the shared `hp-card` style.
  - Sections follow the same pattern on every page:
    - Page header = title + primary actions (and filters) using the shared header layout.
    - Content grouped into `.hp-section` blocks with even spacing.
  - Tables are compact with row hover, minimal borders, and scroll horizontally on small screens.
  - Buttons:
    - One primary blue button per view (filled).
    - Secondary actions as outline/ghost buttons or dropdown menu.

Top-Level Navigation
--------------------

- Logged-in user sees a simple top navigation bar or sidebar with:
  - Hussein Fazio (brand/title).
  - Links:
    - Dashboard.
    - Patients.
    - Appointments.
    - Exercises.
    - Settings.
  - User menu (top-right): shows logged-in user and Logout.

Routing Principles
------------------

- Each major page has a dedicated, bookmarkable route that can be opened directly without navigating from another page.
- Example routes (Django-style paths; exact patterns can vary):
  - Dashboard: `/` or `/dashboard/`.
  - Patients list: `/patients/`.
  - New patient: `/patients/new/`.
  - Patient details: `/patients/<patient_id>/`.
  - Edit patient: `/patients/<patient_id>/edit/`.
  - New visit: `/visits/new/`.
  - Visit details: `/visits/<visit_id>/`.
  - Edit visit: `/visits/<visit_id>/edit/`.
  - Appointments list: `/appointments/`.
  - New appointment: `/appointments/new/`.
  - Exercises list (library): `/exercises/`.
  - Pending payments: `/pending-payments/`.
  - Settings: `/settings/`.
- Navigation elements (links, buttons, cards) should point to these routes, but the routes must also work when accessed directly via the browser address bar.

Home Dashboard (Hussein Fazio)
------------------------------

Page header:

- Title: "Hussain Physio".
- Subtitle: "Clinic dashboard".
- Right-side controls:
  - Date filter dropdown:
    - Options: Today (default), This week, This month, This year, Custom.
    - Affects:
      - Total revenue (card).
      - Visits / Patients (card).
      - Revenue chart.
      - Visits table.
  - Primary button:
    - "+ New visit".
  - Secondary actions (dropdown "More actions"):
    - New patient.
    - New appointment.
    - Complete appointment.

Summary row (cards):

- Card 1: Total revenue (selected period)
  - Shows:
    - Label: "Total revenue (selected period)".
    - Value: sum of all paid amounts in the filtered period.
  - Behavior:
    - Clicking opens a detailed revenue report page or filtered visits list for that period.

- Card 2: Pending amount (all time)
  - Shows:
    - Label: "Pending amount (all time)".
    - Value: total outstanding dues ignoring the date filter.
  - Behavior:
    - Clicking opens a "Pending payments" page listing all visits/patients with unpaid or partially paid amounts.

- Card 3: Visits / Patients (selected period)
  - Shows:
    - Label: "Visits / Patients (selected period)".
    - Value: e.g. "10 visits · 7 patients" within the date filter.

Middle section:

- Left card: Revenue over time
  - Title: "Revenue over time".
  - Content:
    - Bar chart (Chart.js or similar) with x-axis as days/months depending on filter selection.
    - y-axis is revenue.
  - Uses the global date filter to determine the period.

- Right card: Pending payments
  - Title: "Pending payments".
  - Content:
    - Compact table of visits with unpaid or partially paid amounts.
    - Columns:
      - Patient.
      - Visit date.
      - Due amount.
    - Sorted by oldest due first.
  - This table is informational; detailed management happens in the "Pending payments" page reachable via the Pending amount card.

Visits table section:

- Full-width card below the chart and pending payments.
- Header area:
  - Left: filter buttons for visits:
    - Today.
    - This month.
    - This year.
  - Right:
    - Search input for patient name.
  - Filters for this table can follow the global date filter or act as a quick override; simplest is:
    - Global date filter = default range.
    - Within that, quick buttons change the range for the table.
- Table columns:
  - Time/Date.
  - Patient.
  - Payment status (Paid / Pending / Partial).
  - Amount.
  - Actions (e.g. "Open visit").

Export to CSV from dashboard:

- Provide an "Export" dropdown button near the top-right of the Visits table card or summary row:
  - Options:
    - Export visits (current filter) to CSV.
    - Export patients to CSV.
    - Export pending payments to CSV.
- When clicked:
  - Download a CSV file with appropriate columns.
  - Export respects filters where applicable (e.g., visits obey current date filter).

Flows for Adding and Managing Data
----------------------------------

New patient flow:

- Entry points:
  - "More actions" dropdown → "New patient".
  - Patients page → "New patient" button.
- Screen: New patient form page.
  - Fields:
    - Name (required).
    - Mobile number (required).
    - Email (optional).
    - Age, gender, address, notes (optional).
  - Behavior:
    - On submit:
      - Create patient.
      - Redirect to Patient details page.
    - If duplicate mobile is detected:
      - Show a warning and link to existing patient.

New visit (new entry) flow:

- Entry points:
  - Dashboard header: "+ New visit".
  - Patient details page: "+ Add visit".
  - From appointments: "Mark as completed" → "Create visit".
- Screen: New visit form page.
  - Top area:
    - If visit is for an existing patient:
      - Patient selector with search by name/phone.
    - If entered via patient page:
      - Patient is pre-selected and not changeable.
  - Pending dues banner:
    - For existing patients with unpaid/partial visits:
      - Show banner at top with:
        - Total outstanding amount.
        - Short list of last unpaid visits with dates and balances.
  - Fields:
    - Visit date (defaults to today).
    - Symptoms/complaints.
    - Treatment given.
    - Payment:
      - Visit fee (amount owed).
      - Amount paid.
      - Payment method.
      - Payment date (defaults to today).
    - Notes.
    - Next appointment date (optional).
    - Prescribed exercises:
      - Search and select from Exercise library.
  - Behavior:
    - On submit:
      - Create visit, update patient summary, update dues.
      - Optionally redirect to:
        - Visit details page, or
        - Back to patient details with a success message.
    - After save:
      - Provide a visible button "Generate WhatsApp message" on the visit details page.

Follow-up visit flow:

- Main path:
  - Search or navigate to Patient details.
  - Click "+ Add visit".
  - Fill the same visit form as above with the pending dues banner.

New appointment flow:

- Entry points:
  - "More actions" dropdown → "New appointment".
  - Appointments page → "New appointment".
- Screen: Appointment form page or modal.
  - Fields:
    - Patient (existing or new inline).
    - Date and time.
    - Reason/notes.
  - On submit:
    - Create appointment (status = Scheduled).

Complete appointment flow:

- Main path:
  - Appointments page → list of today’s appointments.
  - Each appointment row has "Complete" button.
  - Clicking "Complete":
    - Opens the New visit form with:
      - Patient pre-selected.
      - Date/time pre-filled.
      - Appointment linked to visit.
  - After visit is saved:
    - Appointment status automatically set to Completed.

Patient Pages
-------------

Patients list page:

- Header:
  - Title: "Patients".
  - Actions:
    - "New patient" button.
    - Export patients to CSV.
- Filters and search:
  - Search by name or phone.
  - Optional filter by "Has pending dues".
- Table:
  - Columns:
    - Patient name.
    - Mobile.
    - Last visit date.
    - Pending amount.
    - Actions ("View").

Patient details page:

- Layout:
  - Top summary card with:
    - Name, contact details.
    - First visit date, last visit date.
    - Total visits.
    - Total revenue and pending amount for this patient.
  - Actions:
    - "Edit patient".
    - "+ Add visit" (follow-up).
  - Below summary:
    - Visits list (most recent first).
      - Each row: date, symptoms preview, payment status, amount, link to visit details.

Visit Details Page
------------------

- Header:
  - Visit date, patient name.
  - Link back to patient details.
- Sections:
  - Symptoms and treatment.
  - Payment details (amount, paid, status, method).
  - Notes.
  - Prescribed exercises:
    - List of exercises with links to Google Drive.
- Actions:
  - "Edit visit".
  - "Generate WhatsApp message":
    - Opens a modal showing:
      - Auto-generated message text.
      - Buttons:
        - "Copy message".
        - "Open WhatsApp" (wa.me link with phone and text).

Appointments Pages
------------------

Appointments list page:

- Header:
  - Title: "Appointments".
  - Actions:
    - "New appointment".
- Filters:
  - Tabs or date picker for Today, Upcoming, Past.
- Table:
  - Columns:
    - Date and time.
    - Patient.
    - Reason.
    - Status (Scheduled, Completed, Cancelled, No-show).
    - Actions:
      - "Complete" (opens New visit form).
      - "Mark as no-show".
      - "Cancel".

Exercises Pages
---------------

Exercise library page:

- Header:
  - Title: "Exercises".
  - Actions:
    - "Import from Google Drive" (opens file picker from the shared folder).
- Filters:
  - Search by name.
  - Filter by category/body part.
- Cards or table:
  - For each exercise:
    - Name.
    - Category.
    - Thumbnail or icon indicating type (image/video).
    - "View" button (opens Google Drive).

Attaching exercises in visit form:

- In the visit form:
  - "Add exercises" button.
  - Opens a modal with:
    - Search and filters.
    - List of exercises with checkboxes.
  - Selected exercises appear as tags or list items in the form.

Pending Payments Page
---------------------

- Entry:
  - Click on the Pending amount card on the dashboard.
- Layout:
  - Header:
    - Title: "Pending payments".
    - Actions:
      - Export pending payments to CSV.
  - Filters:
    - Filter by age of dues (e.g., "All / >7 days / >30 days").
  - Table:
    - Columns:
      - Patient.
      - Last visit date with due.
      - Total due amount.
      - Number of visits with dues.
      - Actions ("Open patient").

Settings Page
-------------

- Sections:
  - Clinic details:
    - Clinic name.
    - Owner name.
    - Owner email (for monthly reports).
  - Defaults:
    - Default visit fee (optional).
  - Integrations:
    - Information about Google Drive folder and service account (read-only display if configured in environment).
  - Reports:
    - "Send monthly report now" button to trigger an immediate email for the current/previous month.

Export Flows Summary
--------------------

- Dashboard:
  - Export visits (current filter) to CSV.
  - Export pending payments to CSV.
- Patients page:
  - Export all patients to CSV (not filtered by date).
- Pending payments page:
  - Export current filtered pending dues to CSV.
