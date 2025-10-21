#!/usr/bin/env python3
"""
Fix enum case mismatch in orders table.
Migrates lowercase enum values to uppercase to match the schema.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from config import config

def fix_enum_case():
    """Fix enum case in orders table."""
    
    app_config = config['development']
    database_url = app_config.SQLALCHEMY_DATABASE_URI
    
    print("=" * 60)
    print("Fix Enum Case Migration")
    print("=" * 60)
    print(f"\nConnecting to database...")
    
    try:
        engine = create_engine(database_url, echo=False)
        
        with engine.connect() as conn:
            print("✓ Database connection successful\n")
            
            # Check current enum definition
            result = conn.execute(text("SHOW COLUMNS FROM orders LIKE 'status'"))
            column_info = result.fetchone()
            
            if column_info:
                print(f"Current enum definition: {column_info[1]}\n")
            
            # Check if we have any orders
            result = conn.execute(text("SELECT COUNT(*) FROM orders"))
            order_count = result.scalar()
            print(f"Found {order_count} existing orders\n")
            
            if order_count > 0:
                # Update existing order status values to uppercase
                print("Updating existing order status values to uppercase...")
                
                # Update each status value
                status_map = {
                    'pending': 'PENDING',
                    'validated': 'VALIDATED', 
                    'processing': 'PROCESSING',
                    'completed': 'COMPLETED'
                }
                
                for old_val, new_val in status_map.items():
                    result = conn.execute(text(f"""
                        UPDATE orders 
                        SET status = '{new_val}' 
                        WHERE status = '{old_val}'
                    """))
                    conn.commit()
                    if result.rowcount > 0:
                        print(f"  ✓ Updated {result.rowcount} orders from '{old_val}' to '{new_val}'")
            
            # Alter the enum column definition to uppercase
            print("\nUpdating enum definition to uppercase...")
            
            conn.execute(text("""
                ALTER TABLE orders 
                MODIFY COLUMN status ENUM('PENDING','VALIDATED','PROCESSING','COMPLETED') 
                NOT NULL DEFAULT 'PENDING'
            """))
            conn.commit()
            
            print("✓ Enum definition updated\n")
            
            # Verify the change
            result = conn.execute(text("SHOW COLUMNS FROM orders LIKE 'status'"))
            column_info = result.fetchone()
            
            if column_info:
                print(f"New enum definition: {column_info[1]}\n")
            
            print("=" * 60)
            print("✓ Migration completed successfully!")
            print("=" * 60)
            
            return True
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = fix_enum_case()
    sys.exit(0 if success else 1)
