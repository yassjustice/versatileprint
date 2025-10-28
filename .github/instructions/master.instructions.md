---
applyTo: '**'
---
# Master Build Prompt — Professional Printing Service Platform (Flask + MariaDB)

You are a Senior Full‑Stack Engineer tasked with building a production‑ready web application strictly within the following scope and stack. Use this prompt as the authoritative specification. Do not deviate from the scope, stack, or business rules stated here.


## 1) Role, Scope, and Non‑Negotiables

- Role: Senior Full‑Stack Engineer (Flask + MariaDB + HTML/JS/Bootstrap).
- Objective: Replace a manual, Excel-based process with a centralized, secure, quota‑controlled printing order platform.
- Tech stack (mandatory):
  - Backend: Python 3 + Flask (no heavy backend frameworks beyond Flask and common Flask extensions).
  - Database: MariaDB.
  - Frontend: HTML, CSS, JavaScript, Bootstrap.
  - Email: SMTP via Flask‑Mail (or equivalent standard Flask SMTP library).
- RBAC Roles: Client, Agent, Administrator.
- Business‑critical constraints:
  1) Server‑side quota enforcement is the final authority. Block submissions that exceed available quota.
  2) CSV imports are admin-gated: uploads and validations are performed by Admins before insertion into production tables.
  3) Strict Role‑Based Access Control: Users can only perform actions explicitly permitted by their role.
  4) Data integrity: All data imports require explicit human approval. Maintain audit logs for critical actions.
  5) Follow the UI Style Guide and keep the design eye‑friendly, professional, and consistent.
- Out of scope: Non‑Flask server frameworks, non‑MariaDB databases, SPA frameworks (React/Vue/etc.), cloud‑specific services unless abstracted behind SMTP/standard libs.


## 2) Core Business Capabilities

- Order lifecycle: pending → validated → processing → completed ("traité").
- Quotas (per Client, monthly):
  - Black & White: 3000 prints
  - Color: 2000 prints
  - Top‑up minimum when exhausted: +1000 B&W OR +1000 Color
  - Enforced server‑side at order creation and at CSV import validation time.
- Agent workload limit: Default max 10 active orders. Business rule for increase to 30 requires clarification; implement as configurable with default=10 and optional admin override to 30.
- CSV import: Admins upload CSVs in a dedicated section; Admins validate, correct, approve/reject; only approved data is inserted as Orders.
- Notifications: In‑app + Email on key events (status changes, CSV validated/rejected).
- Reporting: Monthly activity/usage export in CSV, Excel, and PDF.
 - Quota alerts: When a client reaches 80% of monthly usage for B&W or Color, send in-app and email alerts (per threshold crossing, per month).


## 3) Data Model (MariaDB)

Design for referential integrity, unique constraints, and auditability. Use InnoDB, UTC timestamps, and sensible indices.

### 3.1 Tables

1) roles
- id INT PK AUTO_INCREMENT
- name VARCHAR(50) UNIQUE NOT NULL  -- values: 'Client', 'Agent', 'Administrator'

2) users
- id INT PK AUTO_INCREMENT
- email VARCHAR(255) UNIQUE NOT NULL
- password_hash VARCHAR(255) NOT NULL
- full_name VARCHAR(255)
- role_id INT NOT NULL FK → roles.id
- created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
- is_active BOOLEAN NOT NULL DEFAULT TRUE
- INDEX(role_id)

3) client_quotas
- id INT PK AUTO_INCREMENT
- client_id INT NOT NULL FK → users.id (must be role Client)
- month DATE NOT NULL  -- normalized as 'YYYY-MM-01'
- bw_limit INT NOT NULL DEFAULT 3000
- color_limit INT NOT NULL DEFAULT 2000
- bw_used INT NOT NULL DEFAULT 0
- color_used INT NOT NULL DEFAULT 0
- UNIQUE(client_id, month)
- INDEX(client_id, month)

4) quota_topups
- id INT PK AUTO_INCREMENT
- client_id INT NOT NULL FK → users.id
- admin_id INT NOT NULL FK → users.id (Administrator performing top-up)
- bw_added INT NOT NULL DEFAULT 0
- color_added INT NOT NULL DEFAULT 0
- transaction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
- notes TEXT NULL
- CHECK (bw_added >= 0 AND color_added >= 0)
- INDEX(client_id, transaction_date)

5) csv_imports
- id INT PK AUTO_INCREMENT
- uploaded_by INT NOT NULL FK → users.id (must be role Administrator)
- original_filename VARCHAR(255) NOT NULL
- stored_filepath VARCHAR(500) NOT NULL
- status ENUM('pending_validation','validated','rejected') NOT NULL DEFAULT 'pending_validation'
- uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
- validated_by INT NULL FK → users.id (Admin)
- validated_at TIMESTAMP NULL
- notes TEXT NULL  -- optional admin review notes
- INDEX(uploaded_by, status)

6) orders
- id INT PK AUTO_INCREMENT
- client_id INT NOT NULL FK → users.id (must be role Client)
- agent_id INT NULL FK → users.id (Agent who created/owns, NULL if client created)
- status ENUM('pending','validated','processing','completed') NOT NULL DEFAULT 'pending'
- bw_quantity INT NOT NULL DEFAULT 0
- color_quantity INT NOT NULL DEFAULT 0
- paper_dimensions VARCHAR(50) NULL  -- e.g., 'A4', 'A3', '210x297mm'
- paper_type VARCHAR(100) NULL  -- e.g., 'matte', 'glossy', 'standard'
- finishing VARCHAR(100) NULL  -- optional (staple, bind, none)
- created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
- updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP
- import_id INT NULL FK → csv_imports.id
- notes TEXT NULL
- INDEX(client_id, status)
- INDEX(agent_id, status)
- INDEX(import_id)

7) notifications
- id INT PK AUTO_INCREMENT
- user_id INT NOT NULL FK → users.id
- message TEXT NOT NULL
- related_order_id INT NULL FK → orders.id
- is_read BOOLEAN NOT NULL DEFAULT FALSE
- created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
- INDEX(user_id, is_read)

8) audit_logs
- id INT PK AUTO_INCREMENT
- user_id INT NULL FK → users.id  -- NULL for system actions
- action VARCHAR(100) NOT NULL  -- e.g., 'ORDER_STATUS_CHANGE','CSV_VALIDATED','USER_LOGIN'
- details JSON NULL  -- or TEXT if JSON unsupported; store structured context
- created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
- INDEX(action, created_at)

### 3.2 Referential Integrity and Validation Notes
- Enforce FK constraints on all relations.
- For quotas, updates must be transactional using row-level locks (SELECT ... FOR UPDATE) to prevent race conditions on bw_used/color_used.
- Agent active order count = orders with status IN ('pending','validated','processing') assigned to that agent.


## 4) Security, Auth, and RBAC

- Authentication: Email + password with strong hashing (bcrypt/argon2). Session-based auth via Flask-Login or secure session cookies.
- Authorization (RBAC):
  - Client: manage own orders and view quotas/notifications.
  - Agent: manage only orders they own/are authorized for; cannot upload CSV; cannot manage users.
  - Admin: full access; user management, quotas, CSV upload/validation, reporting.
- Input validation: Strict server-side validation on all endpoints and CSV pipelines (email uniqueness checks, phone format normalization when provided, strict type casting, duplicate detection for CSV rows).
- Audit logging: Log authentication events (login success/fail), CSV validation decisions, status transitions, top-ups.
- CSRF protection for form posts.
- Rate limiting for auth endpoints (configurable).


## 5) Quota Enforcement Contract

- Quota check runs server-side before order creation or status transition to 'validated' if needed.
- If bw_quantity or color_quantity would exceed available (limit - used for the month), reject with a clear error.
- Available = (limit + sum(topups_in_month)) - used. Top-ups are applied to the same calendar month as their transaction_date.
- UI must reflect real-time quota guidance; however, server is the source of truth. Client-side hints cannot override server checks.
- Edge cases:
  - Mixed orders with both B&W and Color lines: check each independently.
  - Month boundary: Determine month by order created_at; quotas are per 'YYYY-MM'.
  - Concurrent submissions: Use transactions and row locks when adjusting bw_used/color_used.
 - Quota warnings (near exhaustion): Trigger a warning event when usage crosses a configurable threshold (default 80%) for either B&W or Color in a given month. Emit one notification email/in-app per threshold crossing per month.


## 6) CSV Import and Validation Workflow

- Admin uploads CSV → record in csv_imports (status=pending_validation), file stored on disk with a secure path.
- Admin views pending imports; can preview parsed rows with validation results and per-row errors.
- Admin actions:
  - Validate & Import: For each valid row, create an order subject to server-side quota checks. If a row assigns an Agent (optional), enforce that Agent’s active-order cap; otherwise, agent_id remains NULL.
  - Correct: Admin can adjust fields prior to import.
  - Reject: Mark import as rejected with notes (notify uploader Admin).
- On success, set csv_imports.status='validated', link orders.import_id to csv_imports.id, and write audit logs.

### 6.1 CSV Required Columns (minimum)
- client_identifier: one of (client_id | client_email). Prefer client_id if available.
- bw_quantity: integer >= 0
- color_quantity: integer >= 0
- paper_dimensions: string (e.g., A4/A3/210x297mm)
- paper_type: string (e.g., matte/glossy/standard)
- finishing: optional string (e.g., staple/bind/none)
- notes: optional string
- OPTIONAL: agent_identifier (agent_id | agent_email) to assign order ownership to an Agent; if absent, agent_id is NULL.
- OPTIONAL: client_phone (E.164 or configured national pattern) when present; normalize.
- OPTIONAL: external_order_id (string) for idempotency/deduplication across imports.

Sample header (minimal):
client_id,bw_quantity,color_quantity,paper_dimensions,paper_type,finishing,notes

Sample header (with optional assignments and idempotency):
client_email,agent_email,external_order_id,bw_quantity,color_quantity,paper_dimensions,paper_type,finishing,notes,client_phone

Validation rules:
- At least one of bw_quantity or color_quantity > 0.
- Client must exist and be active. If client_email provided, verify format and ensure unique mapping.
- If agent_identifier provided, user must exist with role=Agent and be active; enforce agent active-order cap.
- Strict numeric casting for quantities; reject non-integers and negatives.
- Telephone validation (if client_phone present): enforce configured pattern and normalize to a canonical format.
- Duplicate detection:
  - Within-file: flag duplicate external_order_id values.
  - Cross-file/database: if external_order_id was previously imported, mark as duplicate (idempotent behavior) or flag for review.
  - Optional heuristic duplicate warning on identical (client, quantities, specs, notes) within a short time window.
- Collect per-row errors; allow Admin to edit rows in UI before import.


## 7) API Surface (REST)

Prefix all endpoints with /api. Responses are JSON. Use standard HTTP status codes. Include pagination (page, page_size), sorting, and filtering where appropriate.

Auth
- POST /api/auth/login  -> {email, password} → 200 {user, token/session} | 401
- POST /api/auth/logout -> 204

Users (Admin only)
- GET  /api/users        -> list users (filter by role, is_active)
- POST /api/users        -> create user {email, password, full_name, role}
- GET  /api/users/:id    -> user detail
- PATCH/PUT /api/users/:id -> update (name, role, active)
- POST /api/users/:id/reset-password -> reset flow

Orders
- GET  /api/orders       -> list (role-filtered)
- POST /api/orders       -> create order (Client or Agent; server enforces quotas and agent cap)
- GET  /api/orders/:id   -> detail (role-filtered)
- PATCH /api/orders/:id  -> update certain fields (Admin/Agent per rules)
- POST /api/orders/:id/status -> change status {status} (enforce allowed transitions and audit)

Quotas (Admin + Client self-view)
- GET  /api/quotas?client_id=&month=YYYY-MM -> fetch quota summary and usage
- POST /api/quotas/topup -> Admin creates top-up {client_id, bw_added, color_added, notes}

CSV Imports (Admin only)
- GET  /api/csv-imports              -> list (Admin)
- POST /api/csv-imports              -> Admin upload (multipart/form-data)
- GET  /api/csv-imports/:id          -> detail + parsed preview (Admin)
- POST /api/csv-imports/:id/validate -> Admin validate & import (with correction payload)
- POST /api/csv-imports/:id/reject   -> Admin reject with notes

Notifications
- GET  /api/notifications            -> list for current user
- POST /api/notifications/:id/read   -> mark as read

Reports (Admin)
- GET  /api/reports/monthly?month=YYYY-MM&format=csv|xlsx|pdf


## 8) Status Transitions

- Allowed transitions:
  - pending → validated (Admin approval or business rule on creation)
  - validated → processing (Admin)
  - processing → completed (Admin)
- Log all transitions to audit_logs with old/new status and actor.
- Notifications to involved Client/Agent on each change.
 - Notifications to involved Client/Agent on each change. For CSV-driven orders, ensure uploader Admin receives outcome notifications.


## 9) Agent Active Order Limit

- Default max_active_orders = 10.
- Configurable system setting (e.g., in config table or env var) allows 30 as an override.
- Count states: pending, validated, processing.
- Block creation/import if creating would exceed Agent’s current cap; return a precise error and include current count.


## 10) Frontend (Bootstrap) – Views and UX

Shared
- Header (consistent across authenticated pages), responsive layout.
- Reusable tables with filtering, sorting, and pagination.
- Dashboard widgets for key metrics.

Client
- Create Order form with real-time quota hints (disable submit if exceeding limits, but server validates definitively).
- Dashboard cards with counts (orders this month, current quotas/usage).
- Orders listing with sorting, filtering, pagination.
- Notifications center.

Agent
- Manage Assigned Orders: table with filters and quick actions (within permissions).
- Create Order for Client (select authorized client); show active order count vs cap.
- No CSV upload capability.

Admin
- Dashboard: counts (pending CSVs, orders by status, quota alerts).
- User Management: CRUD for users and roles; activate/deactivate.
- Quotas: view/edit client quotas, apply top-ups.
- CSV Upload & Validation: Upload files; review pending imports; row-level validation/corrections; approve/reject; import summary with duplicates/quota violations highlighted.
- Reports: Export monthly activity usage (CSV/XLSX/PDF).

Public
- Landing page with marketing presentation; HTML/CSS/JS/Bootstrap only.


## 11) UI Style Guide Compliance (Light Theme)

- Colors (Hex):
  - Primary #118843 (60%), Secondary #1b8811 (30%), Accent #11887e (10%)
  - Background #ffffff, Surface #f8fafc, Text #1e293b, Text Secondary #64748b, Border #e2e8f0
  - Feedback: Success #10b981, Warning #f59e0b, Error #ef4444
- Principles: 60/30/10 usage, soft surfaces for cards/panels, strong readability without harsh contrast.
- Components: Standardized header, pagination, reusable tables, dashboard widgets.
- Real-time feedback on quotas: immediate messaging and disabled actions when exceeding limits.
- Assets: keep images under 200KB, widths 1280–1920px where applicable.
- Charts (Admin reports): only bar/line/area/pie; max 5 slices for pie; clear, legible, spaced.


## 12) Reporting

- Provide Admin exports for a selected month:
  - CSV: standard comma-separated, UTF‑8 with header.
  - Excel (XLSX): proper typing and simple formatting.
  - PDF: clean printable layout (tables/summary). Keep to approved chart types.
- Include: totals per client (B&W, Color), top-ups summary, orders by status, per-agent active order counts.


## 13) Notifications

- In‑app: store in notifications table; list unread first; allow mark-as-read.
- Email: SMTP via Flask‑Mail; templates for order status changes, quota near-exhaustion alerts (80%+), and CSV validation outcomes (approved/rejected with notes). For CSV flows, notify the uploader Admin. If imported rows assign orders to Agents, optionally notify those Agents when orders are created.
- Avoid noisy duplicates; debounce same-event notifications when appropriate.
 - Dedup for quota alerts: only send once per threshold crossing per month (per client, per type B&W/Color).


## 14) Error Handling & Messages

- Standard JSON error envelope: { "error": { "code": "STRING_CODE", "message": "Human readable", "details": {...} } }
- Common codes: AUTH_FAILED, PERMISSION_DENIED, VALIDATION_ERROR, QUOTA_EXCEEDED, AGENT_LIMIT_EXCEEDED, NOT_FOUND, CONFLICT, DUPLICATE_ROW, INVALID_PHONE, INVALID_EMAIL.
- Return actionable messages (e.g., suggest reduce quantity or request top-up when quotas fail).


## 15) Acceptance Criteria (High Level)

- RBAC enforced: Clients cannot see others’ data; Agents restricted to authorized scope; Admin unrestricted.
- Quota enforcement blocks invalid orders (UI shows real-time hints; server enforces final decision).
- CSV workflow: uploads and validations are Admin-only; only validated rows create orders; duplicate detection and strict casting enforced.
- Notifications fire on status changes and CSV outcomes (in-app + email).
- Reporting exports monthly data in CSV/XLSX/PDF.
- Audit logs present for key actions.
- Agent active order cap enforced with clear errors at creation/import.
 - Quota near-exhaustion alerts: when a client’s usage reaches 80% (configurable) for B&W or Color in a month, an in-app notification and an email are sent exactly once per threshold crossing.


## 16) Deliverables

- Working Flask app with MariaDB schema and seed data for roles and an initial admin.
- Schema DDL or migration script; production-ready connection/config handling.
- Minimal theming aligned with the UI Style Guide; Bootstrap-based UI.
- API docs (OpenAPI/Swagger or Markdown) reflecting endpoints and payloads.
- Sample CSV files and validation report examples.
- Basic test coverage for core services: auth, quotas, order creation, CSV import validation path.
- README with setup, env variables, and run steps.


## 17) Configuration & Environment

- Environment variables:
  - DATABASE_URL (MariaDB DSN)
  - SECRET_KEY
  - SMTP settings for email (server, port, username, password, TLS/SSL)
  - MAX_ACTIVE_ORDERS_DEFAULT (default 10)
  - MAX_ACTIVE_ORDERS_OVERRIDE (optional 30)
  - PHONE_VALIDATION_PATTERN (e.g., E.164 regex)
  - CSV_IDEMPOTENCY_MODE (reject|skip|upsert) for handling duplicate external_order_id
  - QUOTA_WARNING_THRESHOLD (default 0.8 for 80%)
- File storage: secure server path for uploaded CSVs, outside web root.
- Timezone: store in UTC; display in user locale if needed.


## 18) Implementation Notes & Guidance

- Use transactions and row-level locking for quota updates to avoid race conditions.
- Centralize RBAC checks (decorators or middleware).
- Centralize quota logic in a service layer; never trust client inputs for quota decisions.
- For performance, index frequent filters: user_id, status, created_at, (client_id, month), (agent_id, status).
- Keep the CSV parser robust: trim whitespace, normalize headers, strict type casting, detect duplicates (within file and against external_order_id history), normalize phone numbers when provided, and provide detailed per-row errors.
- Keep the UI snappy and accessible; progressive enhancement with vanilla JS where helpful.


## 19) Open Business Clarification (Implement Safeguard)

- Agent active order limit escalation from 10 → 30: until clarified, keep as an Admin-configurable override. Expose setting in Admin panel and configuration; default remains 10.


## 20) Minimal Example DDL (Reference)

Note: Use this as a reference; you may implement via migrations. Adjust field lengths/types as needed for MariaDB.

```sql
CREATE TABLE roles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255),
  role_id INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles(id)
) ENGINE=InnoDB;

CREATE TABLE client_quotas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  month DATE NOT NULL,
  bw_limit INT NOT NULL DEFAULT 3000,
  color_limit INT NOT NULL DEFAULT 2000,
  bw_used INT NOT NULL DEFAULT 0,
  color_used INT NOT NULL DEFAULT 0,
  UNIQUE KEY uq_client_month (client_id, month),
  CONSTRAINT fk_cq_client FOREIGN KEY (client_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE quota_topups (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  admin_id INT NOT NULL,
  bw_added INT NOT NULL DEFAULT 0,
  color_added INT NOT NULL DEFAULT 0,
  transaction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  notes TEXT,
  CONSTRAINT fk_qt_client FOREIGN KEY (client_id) REFERENCES users(id),
  CONSTRAINT fk_qt_admin FOREIGN KEY (admin_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE csv_imports (
  id INT AUTO_INCREMENT PRIMARY KEY,
  uploaded_by INT NOT NULL,
  original_filename VARCHAR(255) NOT NULL,
  stored_filepath VARCHAR(500) NOT NULL,
  status ENUM('pending_validation','validated','rejected') NOT NULL DEFAULT 'pending_validation',
  uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  validated_by INT NULL,
  validated_at TIMESTAMP NULL,
  notes TEXT,
  CONSTRAINT fk_ci_uploader FOREIGN KEY (uploaded_by) REFERENCES users(id),
  CONSTRAINT fk_ci_validator FOREIGN KEY (validated_by) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  agent_id INT NULL,
  status ENUM('pending','validated','processing','completed') NOT NULL DEFAULT 'pending',
  bw_quantity INT NOT NULL DEFAULT 0,
  color_quantity INT NOT NULL DEFAULT 0,
  paper_dimensions VARCHAR(50),
  paper_type VARCHAR(100),
  finishing VARCHAR(100),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  import_id INT NULL,
  notes TEXT,
  CONSTRAINT fk_orders_client FOREIGN KEY (client_id) REFERENCES users(id),
  CONSTRAINT fk_orders_agent FOREIGN KEY (agent_id) REFERENCES users(id),
  CONSTRAINT fk_orders_import FOREIGN KEY (import_id) REFERENCES csv_imports(id)
) ENGINE=InnoDB;

CREATE TABLE notifications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  message TEXT NOT NULL,
  related_order_id INT NULL,
  is_read BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_notif_user FOREIGN KEY (user_id) REFERENCES users(id),
  CONSTRAINT fk_notif_order FOREIGN KEY (related_order_id) REFERENCES orders(id)
) ENGINE=InnoDB;

CREATE TABLE audit_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NULL,
  action VARCHAR(100) NOT NULL,
  details JSON NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_audit_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;
```


## 21) Testing (Essentials)

- Unit tests for: auth, RBAC guards, quota calculation and enforcement, order creation, agent cap, CSV parsing/validation path.
- Integration test: end-to-end CSV import → admin validate → orders created → quotas updated → notifications sent.
- Smoke tests for reports export endpoints.


## 22) Definition of Done

- All acceptance criteria met.
- Lint/type checks pass, app starts, basic flows work.
- Database schema created; initial data seeded (roles, an admin, a demo client and agent).
- Documentation complete (API, setup, sample CSVs).
- UI adheres to style guide and provides real-time quota feedback.


— End of Master Build Prompt —