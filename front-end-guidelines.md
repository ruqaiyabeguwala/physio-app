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

- Base colors:
  - Page background: light grey or off-white (e.g. `#f5f5f5` or similar).
  - Card background: white (`#ffffff`).
  - Text color: dark grey/near black (e.g. `#111827` or `#1f2933`).
  - Borders/dividers: very light grey (e.g. `#e5e7eb`).
- Accent colors:
  - Primary: a calm, professional blue/teal (for example, `#2563eb`).
    - Use for primary buttons, active navigation, primary links, and key highlights.
  - Secondary: neutral grey (`#6b7280`) for less prominent buttons and labels.
- Status colors:
  - Success/paid: soft green (e.g. `#16a34a` used lightly).
  - Warning/pending/partial: amber (e.g. `#f59e0b`).
  - Danger/overdue: muted red (e.g. `#dc2626`), used sparingly.
- Usage rules:
  - Do not introduce more accent colors.
  - Use color primarily to communicate meaning (status, selection) and not decoration.

Typography
----------

- Font family:
  - Prefer Inter or Roboto; otherwise use system UI font stack.
- Font sizes:
  - Page title: 20–24 px.
  - Section/card title: 16–18 px.
  - Body text: 14–16 px.
  - Table text and form labels: 13–14 px.
  - Small helper text: 12–13 px.
- Font weights:
  - Normal/regular for most content.
  - Semibold for headings, card titles, table headers, and key numbers.
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

- Appearance:
  - White background.
  - Slight border radius (4–8 px).
  - Very subtle shadow or border to separate from background.
- Content structure:
  - Title row:
    - Left: card title.
    - Right: optional small controls (filters, actions).
  - Body:
    - Key number or chart at the top.
    - Supporting text or table below.
- Examples:
  - Dashboard summary cards (Total revenue, Pending amount, Visits/Patients).
  - Revenue over time chart card.
  - Pending payments card.

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
- Text:
  - Use concise, action-based labels:
    - "New visit", "New patient", "Export CSV", "Complete", "Edit", "Open visit".
- Links:
  - Use primary color for inline links.
  - Underline on hover for clarity.

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
    - Clear primary actions (e.g. "+ Add visit", "Edit").
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
  - Implement these guidelines using a utility-friendly framework like Bootstrap.
  - Where possible, centralize custom styles in a small set of CSS files so the design system is consistent.
- Templates:
  - Use a base Django template defining:
    - Global header/navigation.
    - Main content container.
    - Consistent card and table styles.
  - Individual pages extend the base template and fill defined content blocks.

