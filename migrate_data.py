# migrate_data.py
import sqlite3
from datetime import datetime
from app import create_app, db
from app.models import User, Category, Article, ShoppingList, ShoppingListItem

def migrate_data():
    app = create_app()
    with app.app_context():
        old_conn = sqlite3.connect('shopcart.db')
        old_cur = old_conn.cursor()
        
        try:
            # Bestehende Daten löschen (in der richtigen Reihenfolge wegen Foreign Keys)
            print("Cleaning existing data...")
            ShoppingListItem.query.delete()
            ShoppingList.query.delete()
            Article.query.delete()
            Category.query.delete()
            User.query.delete()
            db.session.commit()
            
            # Users migrieren
            old_cur.execute('SELECT * FROM user')
            users = old_cur.fetchall()
            print(f"Migrating {len(users)} users...")
            for user in users:
                new_user = User(
                    id=user[0],
                    username=user[1],
                    password_hash=user[2],
                    is_admin=user[3],
                    registered_at=datetime.strptime(user[4], '%Y-%m-%d %H:%M:%S.%f'),
                    last_login=datetime.strptime(user[5], '%Y-%m-%d %H:%M:%S.%f') if user[5] else None
                )
                db.session.add(new_user)
            db.session.commit()
            
            # 2. Categories migrieren
            old_cur.execute('SELECT * FROM category')
            categories = old_cur.fetchall()
            print(f"Migrating {len(categories)} categories...")
            for category in categories:
                new_category = Category(
                    id=category[0],       # id
                    name=category[1],     # name
                    icon=category[2],     # icon
                    sort_order=category[3] # sort_order
                )
                db.session.add(new_category)
            db.session.commit()
            
            # 3. Articles migrieren
            old_cur.execute('SELECT * FROM article')
            articles = old_cur.fetchall()
            print(f"Migrating {len(articles)} articles...")
            for article in articles:
                new_article = Article(
                    id=article[0],        # id
                    name=article[1],      # name
                    category_id=article[2] # category_id
                )
                db.session.add(new_article)
            db.session.commit()
            
            # 4. Shopping Lists migrieren
            old_cur.execute('SELECT * FROM shopping_list')
            lists = old_cur.fetchall()
            print(f"Migrating {len(lists)} shopping lists...")
            for lst in lists:
                new_list = ShoppingList(
                    id=lst[0],            # id
                    name=lst[1],          # name
                    user_id=lst[2],       # user_id
                    created_at=lst[3]     # created_at
                )
                db.session.add(new_list)
            db.session.commit()
            
            # 5. Shopping List Items migrieren
            old_cur.execute('SELECT * FROM shopping_list_item')
            items = old_cur.fetchall()
            print(f"Migrating {len(items)} shopping list items...")
            for item in items:
                new_item = ShoppingListItem(
                    shopping_list_id=item[0], # shopping_list_id
                    article_id=item[1],    # article_id
                    quantity=item[2],      # quantity
                    unit=item[3],          # unit
                    notes=item[4],         # notes
                    checked=item[5]        # checked
                )
                db.session.add(new_item)
            db.session.commit()
            
            print("Migration completed successfully!")
            
        except Exception as e:
            print(f"Error during migration: {e}")
            db.session.rollback()
        
        finally:
            old_conn.close()

if __name__ == '__main__':
    migrate_data()