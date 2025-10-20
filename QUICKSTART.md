# VersatilesPrint - Quick Start Guide

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.8+** installed
2. **MariaDB 10.5+** installed and running
3. **pip** (Python package manager)
4. **Git** (optional, for version control)

## Installation Steps

### 1. Navigate to Project Directory

```powershell
cd "d:\New folder\Yassir hakimi\bureau stuff\IT\Projects\ids\VersatilesPrint"
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you encounter a permission error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- Flask and extensions (Flask-Login, Flask-Mail, Flask-CORS)
- SQLAlchemy and PyMySQL (database)
- bcrypt (password hashing)
- Email validation and phone number libraries
- CSV/Excel handling (openpyxl, xlsxwriter)
- PDF generation (reportlab)
- Testing tools (pytest)

### 5. Configure Environment

```powershell
copy .env.example .env
```

Edit `.env` file with your settings:

```ini
# Database Configuration
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/versatiles_print

# SMTP Email Configuration (use Gmail App Password)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Secret Key (generate a random string)
SECRET_KEY=your-very-secret-random-key-here
```

**To generate a secure secret key:**
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### 6. Create MariaDB Database

Open MariaDB client:
```sql
CREATE DATABASE versatiles_print CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or using PowerShell:
```powershell
mysql -u root -p -e "CREATE DATABASE versatiles_print CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 7. Initialize Database Schema

```powershell
python scripts\init_db.py
```

This script will:
- Create all database tables with proper constraints
- Seed initial roles (Client, Agent, Administrator)
- Create default admin account
- Create demo client and agent accounts
- Initialize default quotas

**Default Accounts Created:**
- **Admin**: admin@versatiles.com / Admin123!
- **Client**: client@example.com / Client123!
- **Agent**: agent@example.com / Agent123!

⚠️ **IMPORTANT**: Change these passwords immediately in production!

### 8. Run the Application

```powershell
python run.py
```

The application will start on `http://localhost:5000`

You should see:
```
Starting VersatilesPrint application in development mode...
Server running on http://0.0.0.0:5000
```

### 9. Access the Application

Open your web browser and navigate to:
- **Landing Page**: http://localhost:5000/
- **Login Page**: http://localhost:5000/login
- **API Base**: http://localhost:5000/api/

## Quick Test

### Test 1: Login via API

```powershell
curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{"email":"admin@versatiles.com","password":"Admin123!"}'
```

### Test 2: Create Test Order

First, login and save cookies, then create an order:

```powershell
# Login (save cookies)
curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{"email":"client@example.com","password":"Client123!"}' `
  -c cookies.txt

# Create order (use saved cookies)
curl -X POST http://localhost:5000/api/orders `
  -H "Content-Type: application/json" `
  -b cookies.txt `
  -d '{"bw_quantity":100,"color_quantity":50,"paper_dimensions":"A4","paper_type":"matte","finishing":"none","notes":"Test order"}'
```

### Test 3: Check Quota

```powershell
curl -X GET "http://localhost:5000/api/quotas?client_id=2" -b cookies.txt
```

## Project Structure Overview

```
VersatilesPrint/
├── app/
│   ├── __init__.py              # App factory
│   ├── models/                  # Database models
│   ├── api/                     # REST API endpoints
│   ├── services/                # Business logic
│   ├── templates/               # HTML templates
│   ├── static/                  # CSS, JS, images
│   ├── utils/                   # Helpers, validators
│   └── views.py                 # Web page routes
├── scripts/
│   ├── schema.sql               # Database schema
│   └── init_db.py               # Database initialization
├── samples/                     # Sample CSV files
├── config.py                    # Configuration
├── requirements.txt             # Dependencies
├── run.py                       # Application entry point
└── README.md                    # Full documentation
```

## Common Tasks

### Reset Database

```powershell
# Drop and recreate database
mysql -u root -p -e "DROP DATABASE IF EXISTS versatiles_print; CREATE DATABASE versatiles_print CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Reinitialize
python scripts\init_db.py
```

### Run Tests

```powershell
pytest
```

### View Logs

Logs are stored in the `logs/` directory (created automatically).

### Stop the Server

Press `Ctrl + C` in the terminal where the server is running.

## Troubleshooting

### Issue: "Import could not be resolved" errors in VS Code

**Solution**: These are lint warnings because dependencies aren't installed yet. They'll disappear after running `pip install -r requirements.txt` and reloading VS Code.

### Issue: Database connection failed

**Solution**: 
1. Verify MariaDB is running: `mysql -u root -p`
2. Check DATABASE_URL in `.env` file
3. Ensure database exists: `SHOW DATABASES;`
4. Verify user permissions

### Issue: Port 5000 already in use

**Solution**: Change port in `.env`:
```ini
FLASK_PORT=8000
```

### Issue: Email not sending

**Solution**:
1. For Gmail, use App Passwords (not account password)
2. Enable "Less secure app access" or use OAuth2
3. Check SMTP settings in `.env`
4. Test with a simple email client first

### Issue: Import errors when running scripts

**Solution**: Make sure virtual environment is activated:
```powershell
.\venv\Scripts\Activate.ps1
```

## Next Steps

1. **Change Default Passwords**: Log in and change all default account passwords
2. **Configure Email**: Set up proper SMTP credentials for production
3. **Test CSV Import**: Upload `samples/sample_import_minimal.csv` via admin panel
4. **Explore API**: Read `API_DOCUMENTATION.md` for full API reference
5. **Customize UI**: Modify templates in `app/templates/` and styles in `app/static/css/`
6. **Add Users**: Create real client and agent accounts
7. **Set Up Production**: Configure nginx/Apache reverse proxy, use Gunicorn WSGI server

## Production Deployment Checklist

- [ ] Change SECRET_KEY to a strong random value
- [ ] Set FLASK_ENV=production
- [ ] Set SESSION_COOKIE_SECURE=True (requires HTTPS)
- [ ] Change all default passwords
- [ ] Configure production database with backups
- [ ] Set up proper SMTP email service
- [ ] Use Gunicorn or uWSGI instead of Flask dev server
- [ ] Configure nginx or Apache as reverse proxy
- [ ] Set up SSL/TLS certificates (Let's Encrypt)
- [ ] Enable firewall and security measures
- [ ] Set up monitoring and logging
- [ ] Configure automated backups

## Support

For issues or questions:
1. Check README.md for detailed documentation
2. Review API_DOCUMENTATION.md for API usage
3. Examine error logs in `logs/` directory
4. Check database audit logs for user actions

## License

Proprietary - All rights reserved

---

**You're all set! The VersatilesPrint platform is ready to use.** 🎉
