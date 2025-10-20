"""
SQLite Database Initialization Script for VersatilesPrint
==========================================================
This is a simplified version for development/testing with SQLite.
For production, use MariaDB with scripts/init_db.py instead.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from datetime import datetime
import bcrypt

# SQLite database path
SQLITE_DB_PATH = "instance/versatiles_print.db"

def init_sqlite_database():
    """Initialize SQLite database with simplified schema."""
    
    print("=" * 60)
    print("VersatilesPrint SQLite Database Initialization")
    print("=" * 60)
    print("\n⚠️  WARNING: SQLite is for DEVELOPMENT ONLY!")
    print("For production, use MariaDB with scripts/init_db.py\n")
    
    # Create instance directory
    os.makedirs("instance", exist_ok=True)
    
    # Create SQLite engine
    db_url = f"sqlite:///{SQLITE_DB_PATH}"
    print(f"Database: {SQLITE_DB_PATH}\n")
    
    engine = create_engine(db_url, echo=True)
    
    print("\nCreating tables...")
    
    try:
        with engine.connect() as conn:
            # Simplified schema for SQLite (no CHECK constraints, simplified)
            
            # 1. Roles table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS roles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # 2. Users table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255),
                    phone VARCHAR(20),
                    role_id INTEGER NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (role_id) REFERENCES roles(id)
                )
            """))
            
            # 3. Client quotas table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS client_quotas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER NOT NULL,
                    month DATE NOT NULL,
                    bw_limit INTEGER DEFAULT 3000,
                    color_limit INTEGER DEFAULT 2000,
                    bw_used INTEGER DEFAULT 0,
                    color_used INTEGER DEFAULT 0,
                    bw_alert_sent BOOLEAN DEFAULT 0,
                    color_alert_sent BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES users(id),
                    UNIQUE (client_id, month)
                )
            """))
            
            # 4. Quota topups table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS quota_topups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER NOT NULL,
                    month DATE NOT NULL,
                    bw_topup INTEGER DEFAULT 0,
                    color_topup INTEGER DEFAULT 0,
                    reason TEXT,
                    approved_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES users(id),
                    FOREIGN KEY (approved_by) REFERENCES users(id)
                )
            """))
            
            # 5. CSV imports table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS csv_imports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename VARCHAR(255) NOT NULL,
                    uploaded_by INTEGER NOT NULL,
                    status VARCHAR(50) DEFAULT 'pending_validation',
                    total_rows INTEGER DEFAULT 0,
                    valid_rows INTEGER DEFAULT 0,
                    error_rows INTEGER DEFAULT 0,
                    validation_errors TEXT,
                    validated_by INTEGER,
                    validation_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    validated_at TIMESTAMP,
                    FOREIGN KEY (uploaded_by) REFERENCES users(id),
                    FOREIGN KEY (validated_by) REFERENCES users(id)
                )
            """))
            
            # 6. Orders table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    external_order_id VARCHAR(100) UNIQUE,
                    client_id INTEGER NOT NULL,
                    agent_id INTEGER,
                    bw_count INTEGER DEFAULT 0,
                    color_count INTEGER DEFAULT 0,
                    paper_dimensions VARCHAR(50),
                    orientation VARCHAR(20),
                    additional_options TEXT,
                    status VARCHAR(50) DEFAULT 'pending',
                    csv_import_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES users(id),
                    FOREIGN KEY (agent_id) REFERENCES users(id),
                    FOREIGN KEY (csv_import_id) REFERENCES csv_imports(id)
                )
            """))
            
            # 7. Notifications table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    type VARCHAR(50) DEFAULT 'info',
                    title VARCHAR(255) NOT NULL,
                    message TEXT,
                    is_read BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """))
            
            # 8. Audit logs table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action VARCHAR(100) NOT NULL,
                    table_name VARCHAR(100),
                    record_id INTEGER,
                    details TEXT,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """))
            
            # Create indexes
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_quotas_client ON client_quotas(client_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_orders_client ON orders(client_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_orders_agent ON orders(agent_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id)"))
            
            conn.commit()
            
            print("\n✓ Tables created successfully!")
            
            # Seed data
            print("\nSeeding initial data...")
            
            # Insert roles
            roles = [
                ('Client', 'End-user who submits printing orders'),
                ('Agent', 'Agent who processes printing orders'),
                ('Administrator', 'Admin with full access')
            ]
            
            for name, desc in roles:
                result = conn.execute(text("SELECT id FROM roles WHERE name = :name"), {"name": name})
                if not result.fetchone():
                    conn.execute(text(
                        "INSERT INTO roles (name, description) VALUES (:name, :desc)"
                    ), {"name": name, "desc": desc})
            
            conn.commit()
            
            # Get role IDs
            admin_role = conn.execute(text("SELECT id FROM roles WHERE name = 'Administrator'")).fetchone()[0]
            client_role = conn.execute(text("SELECT id FROM roles WHERE name = 'Client'")).fetchone()[0]
            agent_role = conn.execute(text("SELECT id FROM roles WHERE name = 'Agent'")).fetchone()[0]
            
            # Create default users
            def hash_password(password):
                return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            users = [
                {
                    'email': 'admin@versatiles.com',
                    'password': hash_password('Admin123!'),
                    'full_name': 'System Administrator',
                    'phone': '+1234567890',
                    'role_id': admin_role
                },
                {
                    'email': 'client@example.com',
                    'password': hash_password('Client123!'),
                    'full_name': 'Demo Client',
                    'phone': '+1234567891',
                    'role_id': client_role
                },
                {
                    'email': 'agent@example.com',
                    'password': hash_password('Agent123!'),
                    'full_name': 'Demo Agent',
                    'phone': '+1234567892',
                    'role_id': agent_role
                }
            ]
            
            for user in users:
                result = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": user['email']})
                if not result.fetchone():
                    conn.execute(text("""
                        INSERT INTO users (email, password_hash, full_name, phone, role_id, is_active)
                        VALUES (:email, :password, :full_name, :phone, :role_id, 1)
                    """), {
                        'email': user['email'],
                        'password': user['password'],
                        'full_name': user['full_name'],
                        'phone': user['phone'],
                        'role_id': user['role_id']
                    })
            
            conn.commit()
            
            print("\n✓ Seed data inserted successfully!")
            
            # Display summary
            print("\n" + "=" * 60)
            print("DATABASE INITIALIZATION COMPLETE!")
            print("=" * 60)
            print("\nDefault Users Created:")
            print("-" * 60)
            print(f"{'Role':<15} {'Email':<30} {'Password'}")
            print("-" * 60)
            print(f"{'Administrator':<15} {'admin@versatiles.com':<30} {'Admin123!'}")
            print(f"{'Client':<15} {'client@example.com':<30} {'Client123!'}")
            print(f"{'Agent':<15} {'agent@example.com':<30} {'Agent123!'}")
            print("-" * 60)
            
            print("\n✓ You can now run the application with:")
            print("  python run.py")
            print("\n✓ Access at: http://localhost:5000")
            print("\n⚠️  Remember: SQLite is for DEVELOPMENT ONLY!")
            print("   For production, install MariaDB and use scripts/init_db.py")
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = init_sqlite_database()
    sys.exit(0 if success else 1)
