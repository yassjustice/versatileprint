# Database Installation Guide

## Error: Can't connect to MySQL server on 'localhost'

This means MariaDB/MySQL is not installed or not running on your system.

---

## Solution Options

### Option 1: Install MariaDB (Recommended)

1. **Download MariaDB**:
   - Visit: https://mariadb.org/download/
   - Download the Windows installer (latest stable version)
   - Recommended: MariaDB 10.11 LTS or 11.x

2. **Install MariaDB**:
   - Run the installer
   - Choose "Standard Installation"
   - Set root password (remember this!)
   - Enable "Use UTF8 as default server character set"
   - Install as Windows Service (auto-start)

3. **Verify Installation**:
   ```powershell
   # Check if MariaDB service is running
   Get-Service -Name MariaDB
   
   # Or check MySQL service
   Get-Service -Name MySQL
   ```

4. **Create Database**:
   ```powershell
   # Connect to MariaDB
   mysql -u root -p
   
   # Enter your root password, then run:
   CREATE DATABASE versatiles_print CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'versatiles'@'localhost' IDENTIFIED BY 'YourPassword123!';
   GRANT ALL PRIVILEGES ON versatiles_print.* TO 'versatiles'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

5. **Update .env File**:
   ```ini
   DATABASE_URL=mysql+pymysql://versatiles:YourPassword123!@localhost:3306/versatiles_print
   ```

6. **Initialize Database**:
   ```powershell
   python scripts\init_db.py
   ```

---

### Option 2: Use SQLite (Development Only - Quick Start)

If you just want to test the application quickly without installing MariaDB, you can use SQLite:

1. **Install SQLite Support**:
   ```powershell
   pip install aiosqlite
   ```

2. **Update .env**:
   ```ini
   # Comment out MariaDB URL
   # DATABASE_URL=mysql+pymysql://...
   
   # Use SQLite instead
   DATABASE_URL=sqlite:///instance/versatiles_print.db
   ```

3. **Create Modified Init Script**:
   - SQLite doesn't support all MariaDB features (no CHECK constraints in older versions)
   - You'll need to simplify the schema

**⚠️ Note**: SQLite is NOT recommended for production! It lacks:
- True concurrent write support
- Some SQL features (CHECK constraints, row-level locking)
- Performance at scale

---

### Option 3: Use Docker (Advanced)

1. **Install Docker Desktop for Windows**:
   - Download from: https://www.docker.com/products/docker-desktop

2. **Run MariaDB Container**:
   ```powershell
   docker run -d `
     --name versatiles-mariadb `
     -e MYSQL_ROOT_PASSWORD=root123 `
     -e MYSQL_DATABASE=versatiles_print `
     -e MYSQL_USER=versatiles `
     -e MYSQL_PASSWORD=versatiles123 `
     -p 3306:3306 `
     mariadb:10.11
   ```

3. **Update .env**:
   ```ini
   DATABASE_URL=mysql+pymysql://versatiles:versatiles123@localhost:3306/versatiles_print
   ```

4. **Initialize Database**:
   ```powershell
   python scripts\init_db.py
   ```

---

## Troubleshooting

### MariaDB Service Not Starting

```powershell
# Check service status
Get-Service -Name MariaDB

# Start service manually
Start-Service -Name MariaDB

# Check logs
Get-Content "C:\Program Files\MariaDB *\data\*.err" | Select-Object -Last 50
```

### Connection Refused (Port 3306)

```powershell
# Check if port 3306 is listening
netstat -an | findstr 3306

# If not, check MariaDB configuration
notepad "C:\Program Files\MariaDB *\data\my.ini"

# Ensure these lines exist:
# [mysqld]
# port=3306
# bind-address=127.0.0.1
```

### Access Denied Errors

```powershell
# Reset root password
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED BY 'NewPassword123!';
FLUSH PRIVILEGES;
```

---

## Recommended: Use MariaDB Option 1

For production readiness and full feature support, **install MariaDB natively** using Option 1.

**Download**: https://mariadb.org/download/?t=mariadb&p=mariadb&r=10.11.10&os=windows&cpu=x86_64&pkg=msi
