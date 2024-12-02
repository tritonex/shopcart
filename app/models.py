from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    registered_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime)
    shopping_lists = db.relationship('ShoppingList', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(5), nullable=True)
    sort_order = db.Column(db.Integer, default=999)
    articles = db.relationship('Article', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.icon} {self.name}>'

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artName = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    list_items = db.relationship("ShoppingListItem", back_populates="article")

    def __repr__(self):
        return f'<Article {self.artName}>'

class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="Einkaufsliste", nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    list_items = db.relationship("ShoppingListItem", back_populates="shopping_list", 
                               cascade="all, delete-orphan")

class ShoppingListItem(db.Model):
    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id'), primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), primary_key=True)
    quantity = db.Column(db.String(20))  # War vorher db.Float
    unit = db.Column(db.String(20))
    notes = db.Column(db.String(200))
    checked = db.Column(db.Boolean, default=False)
    
    shopping_list = db.relationship('ShoppingList', back_populates='list_items')
    article = db.relationship('Article', back_populates='list_items')

def create_example_data():
    try:
        if User.query.first() is not None:
            print("Datenbank enthält bereits Daten. Überspringe Beispieldaten.")
            return

        # Admin-User erstellen
        admin = User(username="admin", is_admin=True)
        admin.set_password("admin123")  # Bitte in Produktion ändern!
        db.session.add(admin)
        
        # Normalen User erstellen
        user = User(username="test_user", is_admin=False)
        user.set_password("test123")
        db.session.add(user)
        
        db.session.commit()
        
        # Kategorien erstellen mit Icons und Reihenfolge
        categories = [
            Category(name="Obst & Gemüse", icon="🥬", sort_order=10),
            Category(name="Backwaren", icon="🥨", sort_order=20),
            Category(name="Milchprodukte", icon="🥛", sort_order=30),
            Category(name="Fleisch & Wurst", icon="🥩", sort_order=40),
            Category(name="Tiefkühl", icon="❄️", sort_order=50),
            Category(name="Getränke", icon="🥤", sort_order=60),
            Category(name="Konserven", icon="🥫", sort_order=70),
            Category(name="Süßigkeiten", icon="🍫", sort_order=80),
            Category(name="Gewürze", icon="🧂", sort_order=90),
            Category(name="Reinigung", icon="🧹", sort_order=100),
            Category(name="Hygiene", icon="🧴", sort_order=110)
        ]
        db.session.add_all(categories)
        db.session.commit()

        # Benutzer erstellen
        user = User(username="test_user")
        db.session.add(user)
        db.session.commit()
        
        # Artikel erstellen mit Kategorien
        articles = [
            Article(artName="Milch", category=categories[2]),    # Milchprodukte
            Article(artName="Käse", category=categories[2]),     # Milchprodukte
            Article(artName="Brot", category=categories[1]),     # Backwaren
            Article(artName="Brötchen", category=categories[1]), # Backwaren
            Article(artName="Äpfel", category=categories[0]),    # Obst & Gemüse
            Article(artName="Bananen", category=categories[0]),  # Obst & Gemüse
            Article(artName="Kartoffeln", category=categories[0]), # Obst & Gemüse
            Article(artName="Tomaten", category=categories[0])    # Obst & Gemüse
        ]
        db.session.add_all(articles)
        db.session.commit()
        
        # Einkaufsliste erstellen
        shopping_list = ShoppingList(
            name="Wocheneinkauf", 
            user_id=user.id
        )
        db.session.add(shopping_list)
        db.session.commit()
        
        # Artikel zur Liste hinzufügen
        list_items = [
            ShoppingListItem(
                shopping_list=shopping_list,
                article=articles[0],  # Milch
                quantity=1.0,
                unit="Liter",
                notes="Haltbare Milch"
            ),
            ShoppingListItem(
                shopping_list=shopping_list,
                article=articles[2],  # Brot
                quantity=2,
                unit="Stück",
                notes="Vollkornbrot"
            ),
            ShoppingListItem(
                shopping_list=shopping_list,
                article=articles[4],  # Äpfel
                quantity=1.5,
                unit="kg",
                notes="Bio"
            )
        ]
        db.session.add_all(list_items)
        db.session.commit()
        
        print("Beispieldaten wurden erfolgreich erstellt!")
        
    except Exception as e:
        print(f"Fehler beim Erstellen der Beispieldaten: {e}")
        db.session.rollback()