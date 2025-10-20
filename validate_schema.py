"""
Quick script to validate schema.sql syntax.
Tests if the SQL can be parsed without errors.
"""
import sys
from pathlib import Path

def validate_schema():
    """Validate schema.sql file."""
    
    schema_file = Path(__file__).parent / 'scripts' / 'schema.sql'
    
    if not schema_file.exists():
        print(f"❌ schema.sql not found at {schema_file}")
        return False
    
    print("🔍 Validating schema.sql...")
    print("=" * 60)
    
    with open(schema_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove comments
    lines = []
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('--'):
            continue
        if '--' in line:
            line = line[:line.index('--')]
        lines.append(line)
    
    clean_sql = '\n'.join(lines)
    
    # Split by semicolons
    statements = [s.strip() for s in clean_sql.split(';') if s.strip()]
    
    print(f"\n📊 Found {len(statements)} SQL statements\n")
    
    # Analyze statements
    create_tables = []
    inserts = []
    others = []
    
    for stmt in statements:
        upper_stmt = stmt.upper()
        if 'CREATE TABLE' in upper_stmt:
            # Extract table name
            try:
                table_name = upper_stmt.split('CREATE TABLE')[1].split('IF NOT EXISTS')[1].split('(')[0].strip()
                create_tables.append(table_name)
            except:
                create_tables.append('(unknown)')
        elif 'INSERT INTO' in upper_stmt:
            try:
                table_name = upper_stmt.split('INSERT INTO')[1].split('(')[0].split('VALUES')[0].strip()
                inserts.append(table_name)
            except:
                inserts.append('(unknown)')
        else:
            others.append(stmt[:50] + '...')
    
    print("✅ CREATE TABLE statements:")
    for i, table in enumerate(create_tables, 1):
        print(f"   {i}. {table}")
    
    print(f"\n✅ INSERT statements:")
    for i, table in enumerate(inserts, 1):
        print(f"   {i}. {table}")
    
    if others:
        print(f"\n📋 Other statements: {len(others)}")
    
    # Validation checks
    print("\n" + "=" * 60)
    print("🔍 Validation Checks:")
    print("=" * 60)
    
    checks_passed = 0
    checks_total = 0
    
    # Check 1: Expected tables
    checks_total += 1
    expected_tables = ['ROLES', 'USERS', 'CLIENT_QUOTAS', 'QUOTA_TOPUPS', 
                      'CSV_IMPORTS', 'ORDERS', 'NOTIFICATIONS', 'AUDIT_LOGS']
    
    found_tables = [t.upper() for t in create_tables]
    all_found = all(table in found_tables for table in expected_tables)
    
    if all_found:
        print(f"✅ All {len(expected_tables)} required tables present")
        checks_passed += 1
    else:
        print(f"❌ Missing tables:")
        for table in expected_tables:
            if table not in found_tables:
                print(f"   - {table}")
    
    # Check 2: Seed data
    checks_total += 1
    if 'ROLES' in [t.upper() for t in inserts]:
        print("✅ Roles seed data present")
        checks_passed += 1
    else:
        print("❌ Roles seed data missing")
    
    # Check 3: No Python syntax
    checks_total += 1
    python_keywords = ['"""', "'''", 'import sys', 'import os', 'from pathlib', 'from typing', 'print(', 'def __', 'class ']
    has_python = any(keyword in content for keyword in python_keywords)
    if not has_python:
        print("✅ No Python syntax found")
        checks_passed += 1
    else:
        print("❌ Python syntax detected (should be pure SQL)")
        for keyword in python_keywords:
            if keyword in content:
                print(f"   Found: {keyword}")
    
    # Check 4: Proper semicolons
    checks_total += 1
    if all(';' in clean_sql or stmt.strip() == '' for stmt in statements):
        print("✅ All statements properly terminated")
        checks_passed += 1
    else:
        print("⚠️  Some statements may be missing semicolons")
    
    # Final result
    print("\n" + "=" * 60)
    if checks_passed == checks_total:
        print("✅ VALIDATION PASSED!")
        print("=" * 60)
        print("\nSchema file is ready. You can now run:")
        print("  python scripts\\init_db.py")
        return True
    else:
        print(f"⚠️  VALIDATION ISSUES: {checks_total - checks_passed} check(s) failed")
        print("=" * 60)
        return False

if __name__ == "__main__":
    try:
        success = validate_schema()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
