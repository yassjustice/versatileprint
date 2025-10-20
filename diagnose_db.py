"""
Quick database diagnostic script.
Checks database connectivity and table status.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text, inspect
from config import config
import pymysql

def diagnose_database():
    """Run database diagnostics."""
    
    print("=" * 70)
    print("🔍 VersatilesPrint Database Diagnostic Tool")
    print("=" * 70)
    
    # Get config
    app_config = config['development']
    db_url = app_config.SQLALCHEMY_DATABASE_URI
    
    print(f"\n📋 Configuration:")
    print(f"   Database URL: {db_url.replace(db_url.split(':')[2].split('@')[0], '***') if ':' in db_url and '@' in db_url else db_url}")
    
    # Parse connection details
    try:
        if 'mysql+pymysql://' in db_url:
            parts = db_url.replace('mysql+pymysql://', '').split('/')
            auth_host = parts[0]
            db_name = parts[1].split('?')[0] if len(parts) > 1 else 'versatiles_print'
            
            if '@' in auth_host:
                auth, host = auth_host.split('@')
                if ':' in auth:
                    user, password = auth.split(':')
                else:
                    user = auth
                    password = ''
            else:
                host = auth_host
                user = 'root'
                password = ''
            
            if ':' in host:
                host, port = host.split(':')
                port = int(port)
            else:
                port = 3306
                
        else:
            print("\n⚠️  Not a MySQL/MariaDB connection string")
            return
            
    except Exception as e:
        print(f"\n❌ Error parsing database URL: {e}")
        return
    
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   User: {user}")
    print(f"   Database: {db_name}")
    
    # Test 1: Check if MariaDB/MySQL is running
    print(f"\n🔌 Test 1: Checking if MariaDB/MySQL is reachable...")
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            connect_timeout=5
        )
        print("   ✅ Connection successful!")
        
        # Get server version
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"   Server: {version}")
        cursor.close()
        conn.close()
        
    except pymysql.err.OperationalError as e:
        print(f"   ❌ Cannot connect to server: {e}")
        print("\n💡 Possible fixes:")
        print("   1. Check if MariaDB/MySQL service is running:")
        print("      Get-Service -Name MariaDB")
        print("   2. Start the service:")
        print("      Start-Service -Name MariaDB")
        print("   3. Verify connection settings in .env file")
        return
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        return
    
    # Test 2: Check if database exists
    print(f"\n📂 Test 2: Checking if database '{db_name}' exists...")
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [row[0] for row in cursor.fetchall()]
        
        if db_name in databases:
            print(f"   ✅ Database '{db_name}' exists")
        else:
            print(f"   ❌ Database '{db_name}' NOT FOUND")
            print(f"\n💡 Create the database:")
            print(f"   mysql -u {user} -p -e \"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\"")
            cursor.close()
            conn.close()
            return
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error checking database: {e}")
        return
    
    # Test 3: Check tables
    print(f"\n📊 Test 3: Checking tables in '{db_name}'...")
    try:
        engine = create_engine(db_url, echo=False)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = [
            'roles', 'users', 'client_quotas', 'quota_topups',
            'csv_imports', 'orders', 'notifications', 'audit_logs'
        ]
        
        if not tables:
            print("   ❌ No tables found!")
            print("\n💡 Initialize the database:")
            print("   python scripts\\init_db.py")
            return
        
        print(f"   Found {len(tables)} table(s):")
        
        all_present = True
        for table in required_tables:
            if table in tables:
                print(f"   ✅ {table}")
            else:
                print(f"   ❌ {table} - MISSING")
                all_present = False
        
        if not all_present:
            print("\n💡 Some tables are missing. Reinitialize:")
            print("   python scripts\\init_db.py")
            return
            
    except Exception as e:
        print(f"   ❌ Error checking tables: {e}")
        return
    
    # Test 4: Check seed data
    print(f"\n👥 Test 4: Checking seed data...")
    try:
        with engine.connect() as conn:
            # Check roles
            result = conn.execute(text("SELECT COUNT(*) FROM roles"))
            role_count = result.fetchone()[0]
            print(f"   Roles: {role_count} (expected: 3)")
            
            # Check users
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            print(f"   Users: {user_count} (expected: 3)")
            
            if role_count < 3 or user_count < 3:
                print("\n💡 Seed data incomplete. Reinitialize:")
                print("   python scripts\\init_db.py")
                return
            
            # List users
            result = conn.execute(text("""
                SELECT u.email, r.name 
                FROM users u 
                JOIN roles r ON u.role_id = r.id 
                ORDER BY r.id
            """))
            users = result.fetchall()
            
            print(f"\n   Demo accounts:")
            for email, role in users:
                print(f"   • {role:15} - {email}")
                
    except Exception as e:
        print(f"   ⚠️  Could not check seed data: {e}")
    
    # Final verdict
    print("\n" + "=" * 70)
    print("✅ DATABASE IS PROPERLY CONFIGURED!")
    print("=" * 70)
    print("\n🚀 You can now run the application:")
    print("   python run.py")
    print("\n🌐 Access at: http://localhost:5000")
    print("\n🔐 Login with:")
    print("   Email: admin@versatiles.com")
    print("   Password: Admin123!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        diagnose_database()
    except KeyboardInterrupt:
        print("\n\n⚠️  Diagnostic cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
