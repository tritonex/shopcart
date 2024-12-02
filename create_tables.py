# create_tables.py
from app import create_app, db
from config import Config

def create_tables():
    app = create_app(Config)
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created successfully!")

if __name__ == '__main__':
    create_tables()