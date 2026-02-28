import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "34.27.117.60"),
    "database": os.getenv("DB_NAME", "eamcet_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT", 5432))
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # Get all tables
    cursor.execute("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    print("=== EXISTING TABLES ===")
    for t in tables:
        print(f"  - {t['table_name']}")
    
    # Get mtech_colleges schema
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'mtech_colleges'
    """)
    cols = cursor.fetchall()
    print("\n=== MTECH_COLLEGES SCHEMA ===")
    for c in cols:
        print(f"  {c['column_name']}: {c['data_type']}")
    
    # Sample data
    cursor.execute("SELECT * FROM mtech_colleges LIMIT 3")
    samples = cursor.fetchall()
    print(f"\n=== SAMPLE DATA (first 3 records) ===")
    for s in samples:
        print(f"  {dict(s)}")
    
    # Count data
    cursor.execute("SELECT COUNT(*) as cnt FROM mtech_colleges")
    count = cursor.fetchone()
    print(f"\n=== DATA STATS ===")
    print(f"  Total colleges: {count['cnt']}")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")
