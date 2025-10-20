#!/usr/bin/env python3
"""
Create missing orders and notifications tables.
This script creates only the orders and notifications tables if they don't exist.
"""
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from config import config


def create_missing_tables():
    """Create orders and notifications tables if they don't exist."""
    
    # Get configuration
    app_config = config['development']
    database_url = app_config.SQLALCHEMY_DATABASE_URI
    
    print("=" * 70)
    print("🔧 Creating Missing Tables: orders & notifications")
    print("=" * 70)
    print(f"\nConnecting to database...")
    
    try:
        # Create engine
        engine = create_engine(database_url, echo=False)
        
        with engine.connect() as conn:
            print("✓ Database connection successful\n")
            
            # Check which tables currently exist
            result = conn.execute(text("SHOW TABLES"))
            existing_tables = [row[0] for row in result]
            print(f"📊 Currently existing tables: {len(existing_tables)}")
            for table in sorted(existing_tables):
                print(f"   • {table}")
            
            print("\n" + "-" * 70)
            
            # Create orders table
            print("\n📦 Creating 'orders' table...")
            if 'orders' in existing_tables:
                print("   ⚠️  Table 'orders' already exists. Skipping.")
            else:
                create_orders_sql = """
                CREATE TABLE IF NOT EXISTS orders (
                  id INT AUTO_INCREMENT PRIMARY KEY,
                  client_id INT NOT NULL COMMENT 'Must be Client role',
                  agent_id INT NULL DEFAULT NULL COMMENT 'Agent who created/owns; NULL if client created',
                  status ENUM('pending','validated','processing','completed') NOT NULL DEFAULT 'pending',
                  bw_quantity INT NOT NULL DEFAULT 0,
                  color_quantity INT NOT NULL DEFAULT 0,
                  paper_dimensions VARCHAR(50) DEFAULT NULL COMMENT 'e.g., A4, A3, 210x297mm',
                  paper_type VARCHAR(100) DEFAULT NULL COMMENT 'e.g., matte, glossy, standard',
                  finishing VARCHAR(100) DEFAULT NULL COMMENT 'e.g., staple, bind, none',
                  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
                  import_id INT NULL DEFAULT NULL COMMENT 'FK to csv_imports if from CSV',
                  external_order_id VARCHAR(100) NULL DEFAULT NULL COMMENT 'For idempotency/deduplication',
                  notes TEXT DEFAULT NULL,
                  CONSTRAINT fk_orders_client FOREIGN KEY (client_id) REFERENCES users(id) ON DELETE RESTRICT,
                  CONSTRAINT fk_orders_agent FOREIGN KEY (agent_id) REFERENCES users(id) ON DELETE SET NULL,
                  CONSTRAINT fk_orders_import FOREIGN KEY (import_id) REFERENCES csv_imports(id) ON DELETE SET NULL,
                  INDEX idx_orders_client_status (client_id, status),
                  INDEX idx_orders_agent_status (agent_id, status),
                  INDEX idx_orders_import (import_id),
                  INDEX idx_orders_status (status),
                  INDEX idx_orders_created_at (created_at),
                  INDEX idx_orders_external_id (external_order_id),
                  CHECK (bw_quantity >= 0),
                  CHECK (color_quantity >= 0),
                  CHECK (bw_quantity > 0 OR color_quantity > 0)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """
                
                try:
                    conn.execute(text(create_orders_sql))
                    conn.commit()
                    print("   ✅ Table 'orders' created successfully!")
                except Exception as e:
                    print(f"   ❌ Error creating 'orders' table: {e}")
                    raise
            
            # Create notifications table
            print("\n🔔 Creating 'notifications' table...")
            if 'notifications' in existing_tables:
                print("   ⚠️  Table 'notifications' already exists. Skipping.")
            else:
                create_notifications_sql = """
                CREATE TABLE IF NOT EXISTS notifications (
                  id INT AUTO_INCREMENT PRIMARY KEY,
                  user_id INT NOT NULL,
                  message TEXT NOT NULL,
                  related_order_id INT NULL DEFAULT NULL,
                  is_read BOOLEAN NOT NULL DEFAULT FALSE,
                  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  notification_type VARCHAR(50) DEFAULT 'info' COMMENT 'info, warning, error, success',
                  CONSTRAINT fk_notif_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                  CONSTRAINT fk_notif_order FOREIGN KEY (related_order_id) REFERENCES orders(id) ON DELETE CASCADE,
                  INDEX idx_notif_user_read (user_id, is_read),
                  INDEX idx_notif_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """
                
                try:
                    conn.execute(text(create_notifications_sql))
                    conn.commit()
                    print("   ✅ Table 'notifications' created successfully!")
                except Exception as e:
                    print(f"   ❌ Error creating 'notifications' table: {e}")
                    raise
            
            # Verify tables were created
            print("\n" + "-" * 70)
            print("\n✅ Verification: Checking all tables...")
            result = conn.execute(text("SHOW TABLES"))
            final_tables = [row[0] for row in result]
            
            print(f"\n📊 Total tables now: {len(final_tables)}")
            for table in sorted(final_tables):
                status = "✅" if table in ['orders', 'notifications'] else "  "
                print(f"   {status} {table}")
            
            # Check if our tables are present
            orders_exists = 'orders' in final_tables
            notifications_exists = 'notifications' in final_tables
            
            print("\n" + "=" * 70)
            if orders_exists and notifications_exists:
                print("✅ SUCCESS! Both tables created successfully!")
                print("=" * 70)
                print("\n🚀 Next steps:")
                print("   1. Restart your Flask application")
                print("   2. Test the dashboard at http://127.0.0.1:5000")
                print("   3. Verify /api/orders and /api/notifications endpoints work")
                print("\n💡 The following API endpoints should now work:")
                print("   • GET  /api/orders")
                print("   • POST /api/orders")
                print("   • GET  /api/notifications")
                print("   • POST /api/notifications/mark-read")
                print("=" * 70)
            else:
                print("⚠️  WARNING: Not all tables were created!")
                if not orders_exists:
                    print("   ❌ 'orders' table is missing")
                if not notifications_exists:
                    print("   ❌ 'notifications' table is missing")
                print("=" * 70)
                return False
            
            return True
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("\n⚠️  WARNING: This script will create 'orders' and 'notifications' tables.")
    print("Make sure your database connection is properly configured.\n")
    
    success = create_missing_tables()
    sys.exit(0 if success else 1)
