# 🚀 Quick Setup Guide - MariaDB Database

## Current Issue
```
Error: Table 'versatiles_print.users' doesn't exist
```

## ✅ Solution (3 Steps)

### Step 1: Run Diagnostic
```powershell
python diagnose_db.py
```

This will tell you exactly what's missing.

### Step 2: Initialize Database
```powershell
python scripts\init_db.py
```

### Step 3: Start Application
```powershell
python run.py
```

---

## 📋 Detailed Instructions

### If `diagnose_db.py` shows "Database not found":

```powershell
# Create the database
mysql -u root -p -e "CREATE DATABASE versatiles_print CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Then run init script
python scripts\init_db.py
```

### If `diagnose_db.py` shows "Cannot connect to server":

```powershell
# Check service status
Get-Service -Name MariaDB

# Start service if stopped
Start-Service -Name MariaDB

# Then retry
python diagnose_db.py
```

### If `diagnose_db.py` shows "Access denied":

Edit your `.env` file:
```ini
DATABASE_URL=mysql+pymysql://your_username:your_password@localhost:3306/versatiles_print
```

---

## 🎯 Expected Result

After running `python scripts\init_db.py`, you should see:

```
============================================================
VersatilesPrint Database Initialization
============================================================

Connecting to database...
✓ Database connection successful

Reading schema from schema.sql...
✓ Schema executed successfully

Inserting seed data...
✓ Roles created: Client, Agent, Administrator
✓ Default users created

============================================================
DATABASE INITIALIZATION COMPLETE!
============================================================

Default Users Created:
------------------------------------------------------------
Administrator   admin@versatiles.com    Admin123!
Client          client@example.com      Client123!
Agent           agent@example.com       Agent123!
------------------------------------------------------------
```

---

## 🔄 Multi-Computer Setup

**Important**: If you're using GitHub to sync between computers:

### On Computer 1 (where you just fixed it):
```powershell
git add .
git commit -m "Add database initialization scripts"
git push origin main
```

### On Computer 2 (the one showing the error):
```powershell
# Pull latest code
git pull origin main

# Make sure MariaDB is running
Get-Service -Name MariaDB

# Create database (if needed)
mysql -u root -p -e "CREATE DATABASE versatiles_print CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Initialize tables
python scripts\init_db.py

# Start app
python run.py
```

**Note**: The database itself is NOT synced via Git. Each computer needs its own local database initialized.

---

## 🆘 Still Having Issues?

Run this command and share the output:
```powershell
python diagnose_db.py > diagnosis.txt
```

---

## ✨ After Fix

Once database is initialized, you can:

1. **Access the application**: http://localhost:5000
2. **Login** with:
   - Email: `admin@versatiles.com`
   - Password: `Admin123!`
3. **Create orders, manage users, upload CSV files**

---

## 📁 Files Added/Modified

- `diagnose_db.py` - Database diagnostic tool
- `FIX_DATABASE_ERROR.md` - Detailed troubleshooting guide
- `scripts/init_db.py` - Already exists, creates all tables
- `scripts/schema.sql` - Already exists, SQL schema definition
