Frontend Design Guidelines
==========================

Purpose
-------

- Define a simple, consistent design system for the physio clinic app.
- Make screens easy to scan in a busy clinic environment.
- Ensure the app feels professional and slightly premium without being flashy.

Brand and Layout
----------------

- App title/brand:
  - Use "Hussain Physio" or clinic name consistently in the top navigation and browser title.
- Overall layout:
  - Use a top navigation bar or a slim sidebar with:
    - Brand on the left.
    - Main links: Dashboard, Patients, Appointments, Exercises, Settings.
    - User menu (profile, logout) on the right/top.
  - Page content:
    - Centered within a max-width container.
    - Use cards to group related content (summary, charts, tables, forms).

Colors
------

- Base theme (implemented in `static/css/main.css` and used on all pages):
  - Page background: soft blue/white gradient (`#e3f2fd` → `#ffffff`).
  - Card background: white (`#ffffff`).
  - Text color: dark navy/grey (`#0b1020`).
  - Borders/dividers: subtle blue-tinted grey (`rgba(13, 71, 161, 0.08)`).
- Accent colors:
  - Primary: medical blue (`#0d47a1` with softer variant `#1976d2`).
    - Used for navbar, primary buttons, and key highlights.
  - Secondary: neutral grey/blue (`#607d8b`) for helper text and subtitles.
- Status colors:
  - Success/paid: green gradient (`#43a047` → `#2e7d32`).
  - Warning/pending/partial: amber gradient (`#ffb300` → `#ffa000`).
  - Danger/overdue: red gradient (`#e53935` → `#c62828`).
- Usage rules:
  - Keep the palette limited to these colors for a consistent, calm medical feel.
  - Use color primarily to communicate meaning (status, selection) and not decoration.

Typography
----------

- Font family:
  - Prefer Inter or Roboto; otherwise use system UI font stack.
- Font sizes:
  - Page title: 20–24 px.
  - Section/card title: 16–18 px, slightly larger and bolder than body text.
  - Body text: 14–16 px.
  - Table text and form labels: 13–14 px.
  - Small helper text: 12–13 px.
- Font weights:
  - Normal/regular for most content.
  - Semibold/bold for headings, card titles, table headers, and key numbers.
- Alignment:
  - Left-align text by default.
  - Right-align numeric columns in tables (amounts, counts).

Spacing and Sizing
------------------

- Spacing scale:
  - Base unit: 4 px.
  - Common values:
    - 4 px (tight), 8 px (small), 12 px, 16 px (default), 24 px, 32 px.
- Layout spacing:
  - Page padding: 16–24 px around main content.
  - Spacing between sections (e.g. cards): 16–24 px.
  - Inside cards:
    - Padding: 16 px for standard, 20–24 px for key summary cards.
- Elements:
  - Buttons and inputs:
    - Height: ~36–40 px.
    - Horizontal padding: 10–16 px.
  - Table rows:
    - Vertical padding: 8–10 px for compactness.

Cards
-----

- Appearance (reused across dashboard, patients, visits, appointments, etc.):
  - White background.
  - Rounded corners (around 16–18 px).
  - Very subtle border and soft shadow to separate from background.
- Content structure:
  - Title row:
    - Left: card title in a slightly larger, bold blue style.
    - Right: optional small controls (filters, actions) such as "Edit patient" or "Edit visit" aligned with the related table or data.
  - Body:
    - Key number or chart at the top.
    - Supporting text or table below.
- Implementation:
  - Use the shared `hp-card` class on all card-style containers.
  - For highlighted cards (e.g. Pending amount), use `hp-card hp-card-accent`.
- Examples:
  - Dashboard summary cards (Total revenue, Pending amount, Visits/Patients).
  - Revenue over time chart card.
  - Pending payments card.
  - Patient summary cards on the patient details page.

Buttons and Links
-----------------

- Button types:
  - Primary button:
    - Solid fill using primary color.
    - Used for the main action on the page (e.g. "+ New visit").
  - Secondary button:
    - Outline or ghost style using primary or neutral colors.
    - For less critical actions (e.g. "More actions" trigger, filters).
  - Destructive button:
    - Red outline or red text for actions like delete; use rarely.
- Sizes:
  - Default: medium size (~36–40 px height).
  - Small: for table actions and header controls.
- Icons:
  - Use Bootstrap Icons for common actions:
    - Back: `bi-arrow-left`.
    - Edit: `bi-pencil`.
    - New/add: `bi-plus-lg`, `bi-person-plus`.
    - Export/download: `bi-download`.
    - Open in detail: `bi-box-arrow-up-right`.
    - WhatsApp: `bi-whatsapp`.
  - Pair icons with short labels, and hide labels on very small screens when needed.
- Text:
  - Use concise, action-based labels next to icons:
    - "New visit", "New patient", "Export CSV", "Complete", "Edit", "Open visit", "Generate Whatsapp Receipt".
- Links:
  - Use primary color for inline links.
  - Underline on hover for clarity.
  - For detail and form pages, provide a pill-shaped icon-backed "Back to …" button on the left side of the header to return to the parent list or record.

Forms
-----

- Layout:
  - Use a single-column form layout for most pages.
  - Group related fields under headings (e.g. "Patient details", "Payment").
- Inputs:
  - Use consistent styles:
    - Border-radius aligned with overall design (4–6 px).
    - Light border with clear focus state (border in primary color).
  - Required fields:
    - Mark clearly, e.g. with a small asterisk next to label.
- Validation:
  - Show validation messages just below the field in red text.
  - For errors affecting many fields, consider a brief summary at top.
- Actions:
  - Place primary submit button at the bottom right or bottom center.
  - Use a secondary "Cancel" or "Back" link-style button next to it.

Tables
------

- Table layout:
  - Use full-width responsive tables inside cards.
  - Header row:
    - Slightly bolder/semibold text.
    - Light background (e.g. `#f9fafb`).
  - Body rows:
    - No heavy grid lines; use subtle horizontal dividers between rows.
    - On hover, highlight the row background lightly.
- Columns:
  - Align text:
    - Left-align names and text.
    - Right-align numeric fields and currency.
  - Keep columns minimal and focused on key info.
- Actions:
  - Use a final column for actions like "Open visit", "View", "Edit".
  - Use small buttons or text links, not large buttons in every row.

Charts
------

- Library:
  - Use a lightweight chart library such as Chart.js.
- Styles:
  - Bar charts:
    - Use primary color for bars.
    - Optional lighter variant for comparison or background.
  - Axes and labels:
    - Minimal gridlines; avoid clutter.
    - Short labels (e.g. dates abbreviated).
- Usage:
  - Dashboard revenue chart:
    - Bar chart showing revenue over time for the selected period.
  - Do not add more chart types in MVP beyond what is in the PRD.

States and Feedback
-------------------

- Loading:
  - Use simple spinners or skeleton states inside cards and tables while data loads.
- Empty states:
  - When lists/tables have no data:
    - Show a brief message (e.g. "No patients found") and a relevant action (e.g. "New patient").
- Success:
  - Show a short success alert or toast when key actions complete:
    - "Patient created", "Visit saved", "CSV exported".
- Error:
  - Show clear, non-technical messages for failures:
    - "Unable to save visit. Please try again."
  - In forms, highlight the specific fields causing errors.

Dashboard-Specific Guidelines
-----------------------------

- Header:
  - Title: "Hussain Physio".
  - Right: date filter, "+ New visit", "More actions" dropdown.
- Summary row:
  - Use three equal-width summary cards:
    - Total revenue (filtered by date).
    - Pending amount (all time, not filtered by date).
    - Visits / Patients (filtered by date).
  - Make cards clickable where specified by the app flow (e.g. pending amount → pending payments page).
- Middle section:
  - Left: bar chart of revenue over time.
  - Right: table of pending payments.
- Lower section:
  - Visits table card with:
    - Filter buttons (Today, This month, This year).
    - Search field for patient name.
    - Table of visits with actions.
- Export:
  - Provide an export dropdown tied to the current view or filters for visits and pending payments.

Page Types and Consistency
--------------------------

- Index/list pages (Dashboard, Patients, Appointments, Exercises, Pending payments):
  - Use:
    - Page title + key actions in header.
    - Filters and search below the header.
    - Main list or table in a card.
  - Include export actions where relevant.
- Detail pages (Patient details, Visit details):
  - Use:
    - A summary area at the top in one or more cards.
    - Tabs or sections for related lists (e.g. visits for a patient).
    - A left-aligned back button in the header ("Back to patients" or "Back to patient").
    - Section titles styled consistently using `hp-section-heading` (larger, bold, blue).
    - Contextual actions aligned with the data they control:
      - "Edit patient" in the same row as the patient visits table header.
      - "Edit visit" in the same row as the visit payment section header.
    - A prominent bottom-of-page primary action where needed:
      - On Visit detail, a highlighted "Generate Whatsapp Receipt" button aligned to the bottom right.
- Form pages (New patient, New visit, New appointment):
  - Keep center-aligned, single-column forms.
  - Use grouped sections with headings and adequate spacing.

Accessibility Basics
--------------------

- Contrast:
  - Ensure text and key UI elements have sufficient contrast against backgrounds.
- Focus:
  - All interactive elements (buttons, links, inputs) must have a visible focus state.
- Click targets:
  - Make buttons and clickable icons large enough to tap easily on touch devices.
- Labels:
  - Every form input should have a visible label, not just placeholder text.

Integration with Tech Stack
---------------------------

- CSS:
  - Implement these guidelines using Bootstrap plus a small custom stylesheet:
    - `static/css/main.css` defines palette, spacing, card styles, and animations.
  - Reuse shared classes (`hp-card`, `hp-section`, `hp-page-header`, `hp-page-title`, `hp-page-subtitle`) on every page to keep the theme identical.
- Templates:
  - Use a single base Django template (`templates/base.html`) defining:
    - Global header/navigation.
    - Main content container.
    - Inclusion of Bootstrap and `main.css`.
  - Individual pages extend the base template and:
    - Use the same header pattern (title + primary actions).
    - Wrap major blocks in `.hp-section` and cards in `.hp-card`.
