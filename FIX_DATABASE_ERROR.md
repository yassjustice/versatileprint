# 🔧 Fix: Database Tables Not Found

## Error Summary
```
pymysql.err.ProgrammingError: (1146, "Table 'versatiles_print.users' doesn't exist")
```

**Cause**: The MariaDB database exists but the tables haven't been created yet.

---

## ✅ Solution: Initialize the Database

### Option 1: Run the Initialization Script (Recommended)

Open PowerShell in your project directory and run:

```powershell
python scripts\init_db.py
```

This will:
- Connect to your MariaDB database (`versatiles_print`)
- Execute the schema.sql to create all 8 tables
- Insert seed data (3 roles + 3 demo users)

**Expected Output:**
```
============================================================
VersatilesPrint Database Initialization
============================================================

Connecting to database...
Database URL: localhost:3306/versatiles_print

Executing schema creation...
✓ Tables created successfully!

Seeding initial data...
✓ Seed data inserted successfully!

============================================================
DATABASE INITIALIZATION COMPLETE!
============================================================

Default Users Created:
------------------------------------------------------------
Role            Email                          Password
------------------------------------------------------------
Administrator   admin@versatiles.com           Admin123!
Client          client@example.com             Client123!
Agent           agent@example.com              Agent123!
------------------------------------------------------------
```

---

### Option 2: Manual SQL Execution

If the script doesn't work, run these commands manually:

1. **Open MySQL/MariaDB command line:**
```powershell
mysql -u root -p
```

2. **Use the database:**
```sql
USE versatiles_print;
```

3. **Execute the schema file:**
```powershell
# Exit MySQL first (type 'exit')
mysql -u root -p versatiles_print < scripts\schema.sql
```

4. **Run the initialization script for seed data:**
```powershell
python scripts\init_db.py
```

---

## ⚠️ Troubleshooting

### Issue 1: "Access denied for user"
**Solution**: Update your `.env` file with correct credentials:
```ini
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/versatiles_print
```

### Issue 2: "Unknown database 'versatiles_print'"
**Solution**: Create the database first:
```sql
mysql -u root -p -e "CREATE DATABASE versatiles_print CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### Issue 3: Script fails with import errors
**Solution**: Make sure you're in the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
python scripts\init_db.py
```

### Issue 4: "Can't connect to MySQL server"
**Solution**: 
1. Check if MariaDB/MySQL service is running:
   ```powershell
   Get-Service -Name MariaDB
   # or
   Get-Service -Name MySQL
   ```
2. Start the service if stopped:
   ```powershell
   Start-Service -Name MariaDB
   ```

---

## 🔍 Verify the Fix

After running the initialization, verify tables exist:

```powershell
mysql -u root -p -e "USE versatiles_print; SHOW TABLES;"
```

**Expected output:**
```
+----------------------------+
| Tables_in_versatiles_print |
+----------------------------+
| audit_logs                 |
| client_quotas              |
| csv_imports                |
| notifications              |
| orders                     |
| quota_topups               |
| roles                      |
| users                      |
+----------------------------+
```

---

## 📝 After Fix

Once the database is initialized:

1. **Push changes to GitHub:**
   ```powershell
   git add .
   git commit -m "Initialize database schema"
   git push origin main
   ```

2. **Pull on the other computer:**
   ```powershell
   git pull origin main
   ```

3. **Run the same initialization on the other computer:**
   ```powershell
   python scripts\init_db.py
   ```

4. **Start the application:**
   ```powershell
   python run.py
   ```

5. **Test login at** http://localhost:5000/login with:
   - Email: `admin@versatiles.com`
   - Password: `Admin123!`

---

## 🎯 Quick Command Summary

```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Initialize database
python scripts\init_db.py

# 3. Verify tables
mysql -u root -p -e "USE versatiles_print; SHOW TABLES;"

# 4. Start application
python run.py

# 5. Access application
# Open browser: http://localhost:5000
```

---

## 💡 Note for Multi-Computer Setup

**Important**: Each computer needs to:
1. Have MariaDB/MySQL installed and running
2. Have the `versatiles_print` database created
3. Run `python scripts\init_db.py` to create tables
4. Have the same `.env` configuration

The database is **NOT synced via GitHub** - only the code is synced. Each computer maintains its own local database.

If you want to share data between computers, you'll need to:
- Use a shared remote database server, OR
- Export/import the database using mysqldump
