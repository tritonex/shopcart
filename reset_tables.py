from app import create_app, db
from config import Config

def reset_tables():
    print("Initializing app...")
    app = create_app(Config)
    
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating new tables...")
        db.create_all()
        print("Tables reset successfully!")

if __name__ == '__main__':
    reset_tables()