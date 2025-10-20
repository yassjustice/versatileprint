# VersatilesPrint - Professional Printing Service Platform

A production-ready web application for managing professional printing orders with quota control, role-based access, and CSV bulk imports.

## Features

- **Role-Based Access Control (RBAC)**: Client, Agent, and Administrator roles with strict permissions
- **Quota Management**: Monthly quota enforcement (3000 B&W, 2000 Color) with server-side validation
- **Order Lifecycle**: pending → validated → processing → completed workflow
- **CSV Bulk Import**: Admin-controlled validation and import with duplicate detection
- **Agent Workload Control**: Configurable active order limits (default 10, max 30)
- **Notifications**: In-app and email notifications for status changes and quota alerts
- **Reporting**: Export monthly activity in CSV, Excel, and PDF formats
- **Audit Logging**: Comprehensive audit trail for critical actions

## Tech Stack

- **Backend**: Python 3 + Flask
- **Database**: MariaDB with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Email**: Flask-Mail with SMTP
- **Authentication**: Flask-Login with bcrypt password hashing

## Prerequisites

- Python 3.8 or higher
- MariaDB 10.5 or higher
- pip (Python package manager)

## Installation

### 1. Clone the repository

```bash
cd "d:\New folder\Yassir hakimi\bureau stuff\IT\Projects\ids\VersatilesPrint"
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Copy `.env.example` to `.env` and update with your settings:

```bash
copy .env.example .env
```

Edit `.env` and configure:
- Database connection (DATABASE_URL)
- SMTP settings for email
- Secret key for sessions
- Other application settings

### 6. Create database

Create a MariaDB database:

```sql
CREATE DATABASE versatiles_print CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 7. Initialize database schema

```bash
python scripts/init_db.py
```

This will:
- Create all tables with proper constraints
- Seed initial roles (Client, Agent, Administrator)
- Create a default admin user (admin@versatiles.com / Admin123!)

### 8. Run the application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Default Credentials

**Administrator Account:**
- Email: `admin@versatiles.com`
- Password: `Admin123!`

**Change these credentials immediately after first login!**

## Project Structure

```
VersatilesPrint/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── order.py
│   │   ├── quota.py
│   │   ├── csv_import.py
│   │   ├── notification.py
│   │   └── audit_log.py
│   ├── api/                     # REST API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── orders.py
│   │   ├── quotas.py
│   │   ├── csv_imports.py
│   │   ├── notifications.py
│   │   └── reports.py
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── order_service.py
│   │   ├── quota_service.py
│   │   ├── csv_service.py
│   │   ├── notification_service.py
│   │   ├── report_service.py
│   │   └── audit_service.py
│   ├── templates/               # HTML templates
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── client/
│   │   ├── agent/
│   │   ├── admin/
│   │   └── public/
│   ├── static/                  # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── decorators.py
│       ├── validators.py
│       └── helpers.py
├── scripts/
│   ├── init_db.py              # Database initialization
│   └── seed_data.py            # Sample data seeding
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_orders.py
│   ├── test_quotas.py
│   └── test_csv.py
├── uploads/                     # File uploads (git-ignored)
│   └── csv/
├── config.py                    # Configuration
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore
├── run.py                       # Application entry point
└── README.md
```

## API Documentation

### Authentication

- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Users (Admin only)

- `GET /api/users` - List users
- `POST /api/users` - Create user
- `GET /api/users/:id` - Get user details
- `PATCH /api/users/:id` - Update user
- `POST /api/users/:id/reset-password` - Reset password

### Orders

- `GET /api/orders` - List orders (role-filtered)
- `POST /api/orders` - Create order
- `GET /api/orders/:id` - Get order details
- `PATCH /api/orders/:id` - Update order
- `POST /api/orders/:id/status` - Change order status

### Quotas

- `GET /api/quotas` - Get quota information
- `POST /api/quotas/topup` - Create quota top-up (Admin)

### CSV Imports (Admin only)

- `GET /api/csv-imports` - List imports
- `POST /api/csv-imports` - Upload CSV
- `GET /api/csv-imports/:id` - Get import details
- `POST /api/csv-imports/:id/validate` - Validate and import
- `POST /api/csv-imports/:id/reject` - Reject import

### Notifications

- `GET /api/notifications` - List notifications
- `POST /api/notifications/:id/read` - Mark as read

### Reports (Admin)

- `GET /api/reports/monthly` - Export monthly report

## CSV Import Format

### Minimal Format

```csv
client_id,bw_quantity,color_quantity,paper_dimensions,paper_type,finishing,notes
1,100,50,A4,matte,none,Standard order
2,200,0,A3,glossy,staple,Color brochure
```

### Extended Format (with optional fields)

```csv
client_email,agent_email,external_order_id,bw_quantity,color_quantity,paper_dimensions,paper_type,finishing,notes,client_phone
client1@example.com,agent1@example.com,EXT001,100,50,A4,matte,none,Standard order,+1234567890
client2@example.com,,EXT002,200,0,A3,glossy,staple,Color brochure,+1987654321
```

### Validation Rules

- At least one of `bw_quantity` or `color_quantity` must be > 0
- Client must exist and be active
- If agent specified, must exist with Agent role and be active
- Quantities must be non-negative integers
- Duplicate `external_order_id` values are flagged
- Phone numbers validated against E.164 pattern (when provided)

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## Configuration

### Quota Settings

- Default B&W limit: 3000 prints/month
- Default Color limit: 2000 prints/month
- Minimum top-up: 1000 prints
- Warning threshold: 80% usage

### Agent Workload

- Default active order limit: 10
- Maximum override: 30
- Active statuses: pending, validated, processing

### Security

- Password hashing: bcrypt
- Session management: Flask-Login
- CSRF protection: enabled
- Rate limiting: configurable per endpoint

## Deployment

### Production Checklist

1. Set `FLASK_ENV=production` in `.env`
2. Use a strong, random `SECRET_KEY`
3. Configure production database with proper credentials
4. Set `SESSION_COOKIE_SECURE=True` for HTTPS
5. Configure proper SMTP settings
6. Set up reverse proxy (nginx/Apache)
7. Use a production WSGI server (gunicorn/uWSGI)
8. Enable database backups
9. Configure logging and monitoring
10. Review and adjust rate limits

### Example with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## UI Style Guide

### Color Palette

- **Primary**: #118843 (60% usage)
- **Secondary**: #1b8811 (30% usage)
- **Accent**: #11887e (10% usage)
- **Background**: #ffffff
- **Surface**: #f8fafc
- **Text**: #1e293b
- **Text Secondary**: #64748b
- **Border**: #e2e8f0
- **Success**: #10b981
- **Warning**: #f59e0b
- **Error**: #ef4444

### Principles

- Clean, professional appearance
- High readability without harsh contrast
- Consistent spacing and alignment
- Responsive design for all screen sizes
- Real-time feedback for user actions

## Troubleshooting

### Database connection issues

- Verify MariaDB is running
- Check DATABASE_URL in `.env`
- Ensure database exists and user has permissions

### Email not sending

- Verify SMTP credentials
- Check firewall/antivirus settings
- For Gmail, use App Passwords (not account password)

### Import errors

- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version (3.8+ required)

## Support

For issues and questions:
1. Check existing documentation
2. Review error logs in `logs/` directory
3. Consult API documentation
4. Contact system administrator

## License

Proprietary - All rights reserved

## Changelog

### Version 1.0.0 (Initial Release)
- Complete RBAC system with 3 roles
- Order management with quota enforcement
- CSV bulk import with validation
- Notification system (in-app + email)
- Monthly reporting (CSV, Excel, PDF)
- Audit logging
- Bootstrap-based UI with style guide compliance
