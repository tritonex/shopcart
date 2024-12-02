import os
import psycopg2

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    # Verbindungstest beim Start
    try:
        conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
        print("Database connection successful!")
        conn.close()
    except Exception as e:
        print(f"Database connection failed: {e}")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'