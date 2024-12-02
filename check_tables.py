# check_tables.py
import psycopg2
from config import Config

def check_tables():
    try:
        conn = psycopg2.connect(Config.SQLALCHEMY_DATABASE_URI)
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = cur.fetchall()
        print("Existierende Tabellen:")
        for table in tables:
            print(table[0])
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == '__main__':
    check_tables()