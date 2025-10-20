# ✅ Database Setup Checklist

Print this and follow step by step!

---

## 🎯 Goal
Fix the error: "Table 'versatiles_print.users' doesn't exist"

---

## 📝 Prerequisites

- [ ] Virtual environment is activated (`.\venv\Scripts\Activate.ps1`)
- [ ] MariaDB/MySQL is installed
- [ ] You're in the project directory

---

## 🔧 Step-by-Step Fix

### Step 1: Check Database Service
```powershell
Get-Service -Name MariaDB
```
- [ ] Service is running (Status: Running)
- [ ] If not running: `Start-Service -Name MariaDB`

### Step 2: Verify Database Exists
```powershell
mysql -u root -p -e "SHOW DATABASES;"
```
- [ ] `versatiles_print` appears in the list
- [ ] If not: `mysql -u root -p -e "CREATE DATABASE versatiles_print CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"`

### Step 3: Run Diagnostic
```powershell
python diagnose_db.py
```
- [ ] All tests pass (green checkmarks)
- [ ] If issues found, follow the recommendations

### Step 4: Initialize Database Tables
```powershell
python scripts\init_db.py
```
**Expected Output:**
- [ ] "✓ Database connection successful"
- [ ] "✓ Schema executed successfully"
- [ ] "✓ Roles created: Client, Agent, Administrator"
- [ ] "✓ Default users created"
- [ ] Shows 3 demo accounts

### Step 5: Verify Tables Created
```powershell
mysql -u root -p -e "USE versatiles_print; SHOW TABLES;"
```
**Should show 8 tables:**
- [ ] audit_logs
- [ ] client_quotas
- [ ] csv_imports
- [ ] notifications
- [ ] orders
- [ ] quota_topups
- [ ] roles
- [ ] users

### Step 6: Test Application
```powershell
python run.py
```
- [ ] Server starts without errors
- [ ] No "Table doesn't exist" errors
- [ ] Access http://localhost:5000
- [ ] Landing page loads

### Step 7: Test Login
Navigate to: http://localhost:5000/login

Try logging in:
- [ ] Email: `admin@versatiles.com`
- [ ] Password: `Admin123!`
- [ ] Login succeeds
- [ ] Dashboard loads

---

## 🎉 Success Indicators

✅ No database errors in terminal
✅ Login page loads without 500 error
✅ Can authenticate with demo account
✅ Dashboard displays correctly
✅ Can create orders (for clients)
✅ Can view orders (for admins/agents)

---

## 🆘 If Something Goes Wrong

### Error: "Can't connect to MySQL server"
```powershell
# Check if service is running
Get-Service -Name MariaDB

# Restart service
Restart-Service -Name MariaDB
```

### Error: "Access denied for user"
Check your `.env` file and update:
```ini
DATABASE_URL=mysql+pymysql://correct_username:correct_password@localhost:3306/versatiles_print
```

### Error: "Unknown database"
```powershell
mysql -u root -p -e "CREATE DATABASE versatiles_print CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### Tables exist but login still fails
```powershell
# Drop and recreate
mysql -u root -p -e "DROP DATABASE versatiles_print;"
mysql -u root -p -e "CREATE DATABASE versatiles_print CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
python scripts\init_db.py
```

---

## 🔄 For Second Computer

After fixing on Computer 1:

### Computer 1:
```powershell
git add .
git commit -m "Add database setup tools"
git push origin main
```

### Computer 2:
```powershell
git pull origin main
```

Then follow this checklist from Step 1!

---

## 📞 Quick Commands Reference

| Task | Command |
|------|---------|
| Activate venv | `.\venv\Scripts\Activate.ps1` |
| Check service | `Get-Service -Name MariaDB` |
| Start service | `Start-Service -Name MariaDB` |
| Create database | `mysql -u root -p -e "CREATE DATABASE versatiles_print CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"` |
| Run diagnostic | `python diagnose_db.py` |
| Initialize DB | `python scripts\init_db.py` |
| Start app | `python run.py` |
| Access app | http://localhost:5000 |

---

## 📅 Maintenance

Run diagnostic monthly:
```powershell
python diagnose_db.py
```

Backup database weekly:
```powershell
mysqldump -u root -p versatiles_print > backup_$(Get-Date -Format 'yyyy-MM-dd').sql
```

---

**Date Created:** October 20, 2025
**Version:** 1.0
**Status:** Ready for use ✅
