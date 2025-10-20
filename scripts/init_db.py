#!/usr/bin/env python3
"""
Database initialization script.
Creates all tables, indexes, and seeds initial data.
"""
import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
import bcrypt
from sqlalchemy import create_engine, text
from config import config

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def init_database():
    """Initialize the database with schema and seed data."""
    
    # Get configuration
    app_config = config['development']
    database_url = app_config.SQLALCHEMY_DATABASE_URI
    
    print("=" * 60)
    print("VersatilesPrint Database Initialization")
    print("=" * 60)
    print(f"\nConnecting to database...")
    print(f"Database URL: {database_url.split('@')[1] if '@' in database_url else database_url}")
    
    try:
        # Create engine
        engine = create_engine(database_url, echo=False)
        
        with engine.connect() as conn:
            print("\n✓ Database connection successful")
            
            # Read and execute SQL schema
            schema_file = Path(__file__).parent / 'schema.sql'
            
            if not schema_file.exists():
                print(f"\n✗ Error: schema.sql not found at {schema_file}")
                return False
            
            print(f"\nReading schema from {schema_file.name}...")
            
            with open(schema_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Split by semicolons and execute each statement
            statements = [s.strip() for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]
            
            print(f"\nExecuting {len(statements)} SQL statements...")
            
            for i, statement in enumerate(statements, 1):
                # Skip comments
                if statement.startswith('--') or statement.startswith('/*'):
                    continue
                
                try:
                    conn.execute(text(statement))
                    conn.commit()
                except Exception as e:
                    # Continue on duplicate key errors (for idempotent runs)
                    if 'duplicate' not in str(e).lower():
                        print(f"\n  Warning on statement {i}: {str(e)[:100]}")
            
            print("✓ Schema created successfully")
            
            # Seed initial data
            print("\nSeeding initial data...")
            
            # Get role IDs
            result = conn.execute(text("SELECT id, name FROM roles"))
            roles = {row[1]: row[0] for row in result}
            
            if not roles:
                print("✗ Error: No roles found. Schema may not have been created correctly.")
                return False
            
            print(f"  Found roles: {', '.join(roles.keys())}")
            
            # Check if admin already exists
            result = conn.execute(text("SELECT COUNT(*) FROM users WHERE email = 'admin@versatiles.com'"))
            admin_exists = result.scalar() > 0
            
            if not admin_exists:
                # Create default administrator
                admin_password = hash_password('Admin123!')
                admin_role_id = roles['Administrator']
                
                conn.execute(text("""
                    INSERT INTO users (email, password_hash, full_name, role_id, is_active, created_at)
                    VALUES (:email, :password_hash, :full_name, :role_id, :is_active, :created_at)
                """), {
                    'email': 'admin@versatiles.com',
                    'password_hash': admin_password,
                    'full_name': 'System Administrator',
                    'role_id': admin_role_id,
                    'is_active': True,
                    'created_at': datetime.utcnow()
                })
                conn.commit()
                print("  ✓ Created default administrator account")
                print("    Email: admin@versatiles.com")
                print("    Password: Admin123!")
                print("    ⚠ CHANGE THIS PASSWORD IMMEDIATELY!")
            else:
                print("  ℹ Administrator account already exists")
            
            # Create sample client (optional)
            result = conn.execute(text("SELECT COUNT(*) FROM users WHERE email = 'client@example.com'"))
            client_exists = result.scalar() > 0
            
            if not client_exists:
                client_password = hash_password('Client123!')
                client_role_id = roles['Client']
                
                conn.execute(text("""
                    INSERT INTO users (email, password_hash, full_name, role_id, is_active, created_at)
                    VALUES (:email, :password_hash, :full_name, :role_id, :is_active, :created_at)
                """), {
                    'email': 'client@example.com',
                    'password_hash': client_password,
                    'full_name': 'Demo Client',
                    'role_id': client_role_id,
                    'is_active': True,
                    'created_at': datetime.utcnow()
                })
                conn.commit()
                print("  ✓ Created demo client account")
                print("    Email: client@example.com")
                print("    Password: Client123!")
            
            # Create sample agent (optional)
            result = conn.execute(text("SELECT COUNT(*) FROM users WHERE email = 'agent@example.com'"))
            agent_exists = result.scalar() > 0
            
            if not agent_exists:
                agent_password = hash_password('Agent123!')
                agent_role_id = roles['Agent']
                
                conn.execute(text("""
                    INSERT INTO users (email, password_hash, full_name, role_id, is_active, created_at)
                    VALUES (:email, :password_hash, :full_name, :role_id, :is_active, :created_at)
                """), {
                    'email': 'agent@example.com',
                    'password_hash': agent_password,
                    'full_name': 'Demo Agent',
                    'role_id': agent_role_id,
                    'is_active': True,
                    'created_at': datetime.utcnow()
                })
                conn.commit()
                print("  ✓ Created demo agent account")
                print("    Email: agent@example.com")
                print("    Password: Agent123!")
            
            # Initialize quota for demo client if exists
            result = conn.execute(text("SELECT id FROM users WHERE email = 'client@example.com'"))
            client_row = result.fetchone()
            
            if client_row:
                client_id = client_row[0]
                current_month = datetime.utcnow().replace(day=1).date()
                
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM client_quotas 
                    WHERE client_id = :client_id AND month = :month
                """), {'client_id': client_id, 'month': current_month})
                
                quota_exists = result.scalar() > 0
                
                if not quota_exists:
                    conn.execute(text("""
                        INSERT INTO client_quotas (client_id, month, bw_limit, color_limit, bw_used, color_used)
                        VALUES (:client_id, :month, :bw_limit, :color_limit, 0, 0)
                    """), {
                        'client_id': client_id,
                        'month': current_month,
                        'bw_limit': app_config.DEFAULT_BW_LIMIT,
                        'color_limit': app_config.DEFAULT_COLOR_LIMIT
                    })
                    conn.commit()
                    print(f"  ✓ Initialized quota for demo client (month: {current_month})")
            
            print("\n" + "=" * 60)
            print("✓ Database initialization completed successfully!")
            print("=" * 60)
            print("\nYou can now run the application with:")
            print("  python run.py")
            print("\nDefault login credentials:")
            print("  Admin:  admin@versatiles.com / Admin123!")
            print("  Client: client@example.com / Client123!")
            print("  Agent:  agent@example.com / Agent123!")
            print("\n⚠ Remember to change default passwords in production!")
            print("=" * 60)
            
            return True
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
