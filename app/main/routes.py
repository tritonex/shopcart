from flask import Flask, render_template, flash, redirect, url_for, request, make_response, jsonify
from flask_login import current_user, login_required
from datetime import datetime, timezone
from app.main import bp
from app.models import ShoppingList, Article, Category, ShoppingListItem, User
from app.main.forms import ShoppingListForm, AddToListForm, ArticleForm, CategoryForm
from app.extensions import db
from app.utils import admin_required
import random

from flask_migrate import Migrate
from app.extensions import db
from config import Config

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    # ... andere Konfigurationen ...
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    return app

@bp.after_request
def add_header(response):
    if '/admin/' in request.path:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
    return response

@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        shopping_lists = ShoppingList.query.filter_by(
            user_id=current_user.id
        ).order_by(
            ShoppingList.created_at.desc()
        ).all()
        return render_template('index.html', 
                             title='Meine Einkaufslisten',
                             shopping_lists=shopping_lists)
    return render_template('index.html', title='Willkommen')


@bp.route('/shopping_list/new', methods=['GET', 'POST'])
@login_required
def shopping_list_new():
    form = ShoppingListForm()
    if form.validate_on_submit():
        shopping_list = ShoppingList(
            name=form.name.data,
            user_id=current_user.id
        )
        db.session.add(shopping_list)
        db.session.commit()
        flash(f'Einkaufsliste "{shopping_list.name}" wurde erstellt.', 'success')
        return redirect(url_for('main.shopping_list_edit', id=shopping_list.id))
    return render_template('main/shopping_list_form.html', 
                         title='Neue Einkaufsliste',
                         form=form)
    
@bp.route('/shopping_list/item/<int:list_id>/<int:article_id>/update', methods=['POST'])
@login_required
def shopping_list_item_update(list_id, article_id):
    item = ShoppingListItem.query.get_or_404((list_id, article_id))
    if item.shopping_list.user_id != current_user.id:
        flash('Sie können nur Artikel in Ihren eigenen Listen bearbeiten.', 'danger')
        return redirect(url_for('main.index'))

    quantity = request.form.get('quantity', '').strip()
    if quantity:
        item.quantity = quantity  # Direkte Übernahme des Strings
        item.unit = request.form.get('unit')
    else:
        item.quantity = None
        item.unit = None
    
    item.notes = request.form.get('notes', '')
    db.session.commit()
    flash('Artikel wurde aktualisiert.', 'success')
    
    return redirect(url_for('main.shopping_list_edit', id=list_id))
    
@bp.route('/shopping_list/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def shopping_list_edit(id):
    shopping_list = ShoppingList.query.get_or_404(id)
    if shopping_list.user_id != current_user.id:
        flash('Sie können nur Ihre eigenen Listen bearbeiten.', 'danger')
        return redirect(url_for('main.index'))
    
    form = AddToListForm()
    
    # Kategorien für die Artikelauswahl laden
    categories = Category.query.order_by(Category.sort_order).all()
    
    # Set von bereits hinzugefügten Artikel-IDs erstellen
    added_article_ids = {item.article_id for item in shopping_list.list_items}
    
    return render_template('main/shopping_list_edit.html',
                         title=f'Liste bearbeiten: {shopping_list.name}',
                         shopping_list=shopping_list,
                         categories=categories,
                         added_article_ids=added_article_ids,
                         form=form)

@bp.route('/shopping_list/<int:id>/delete', methods=['POST'])
@login_required
def shopping_list_delete(id):
    shopping_list = ShoppingList.query.get_or_404(id)
    if shopping_list.user_id != current_user.id:
        flash('Sie können nur Ihre eigenen Listen löschen.', 'danger')
        return redirect(url_for('main.index'))
    
    name = shopping_list.name
    db.session.delete(shopping_list)
    db.session.commit()
    flash(f'Liste "{name}" wurde gelöscht.', 'success')
    return redirect(url_for('main.index'))

# Route zum direkten Hinzufügen von Artikeln
@bp.route('/shopping_list/<int:list_id>/add/<int:article_id>', methods=['POST'])
@login_required
def shopping_list_add_article(list_id, article_id):
    shopping_list = ShoppingList.query.get_or_404(list_id)
    if shopping_list.user_id != current_user.id:
        return jsonify({
            'success': False,
            'message': 'Sie können nur Ihre eigenen Listen bearbeiten.',
            'category': 'danger'
        })
    
    existing_item = ShoppingListItem.query.filter_by(
        shopping_list_id=list_id,
        article_id=article_id
    ).first()
    
    if existing_item:
        return jsonify({
            'success': False,
            'message': 'Artikel bereits in der Liste.',
            'category': 'warning'
        })
    
    try:
        item = ShoppingListItem(
            shopping_list_id=list_id,
            article_id=article_id
        )
        db.session.add(item)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Artikel wurde zur Liste hinzugefügt.',
            'category': 'success'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Fehler beim Hinzufügen des Artikels.',
            'category': 'danger'
        })

# Route zum Entfernen von Artikeln
@bp.route('/shopping_list/item/<int:list_id>/<int:article_id>/remove', methods=['POST'])
@login_required
def shopping_list_item_remove(list_id, article_id):
    item = ShoppingListItem.query.get_or_404((list_id, article_id))
    if item.shopping_list.user_id != current_user.id:
        flash('Sie können nur Artikel aus Ihren eigenen Listen entfernen.', 'danger')
        return redirect(url_for('main.index'))
    
    db.session.delete(item)
    db.session.commit()
    flash('Artikel wurde aus der Liste entfernt.', 'success')
    return redirect(url_for('main.shopping_list_edit', id=list_id))

# Route zum Abhaken von Artikeln
@bp.route('/shopping_list/item/<int:list_id>/<int:article_id>/toggle', methods=['POST'])
@login_required
def shopping_list_item_toggle(list_id, article_id):
    item = ShoppingListItem.query.get_or_404((list_id, article_id))
    if item.shopping_list.user_id != current_user.id:
        flash('Sie können nur Artikel in Ihren eigenen Listen abhaken.', 'danger')
        return redirect(url_for('main.index'))
    
    item.checked = not item.checked
    db.session.commit()
    
    # Zurück zur richtigen Seite basierend auf dem source Parameter
    source = request.args.get('source', 'edit')
    if source == 'shop':
        return redirect(url_for('main.shopping_list_shop', id=list_id))
    else:
        return redirect(url_for('main.shopping_list_edit', id=list_id))

@bp.route('/shopping_list/<int:id>/shop', methods=['GET'])
@login_required
def shopping_list_shop(id):
    shopping_list = ShoppingList.query.get_or_404(id)
    if shopping_list.user_id != current_user.id:
        flash('Sie können nur Ihre eigenen Listen verwenden.', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('main/shopping.html',
                         title=f'Einkaufen: {shopping_list.name}',
                         shopping_list=shopping_list)

@bp.route('/admin/categories')
@login_required
@admin_required
def category_list():
    categories = Category.query.order_by(Category.sort_order).all()
    return render_template('main/category_list.html',
                         title='Kategorien',
                         categories=categories)


@bp.route('/admin/category/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def category_edit(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        try:
            category.name = form.name.data
            category.icon = form.icon.data
            category.sort_order = form.sort_order.data
            db.session.commit()
            flash(f'Kategorie "{category.name}" wurde aktualisiert.', 'success')
            response = make_response(redirect(url_for('main.category_list')))
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response
        except Exception as e:
            db.session.rollback()
            flash('Fehler beim Speichern der Kategorie.', 'danger')
            
    return render_template('main/category_form.html', 
                         title='Kategorie bearbeiten',
                         form=form)

@bp.route('/admin/category/add', methods=['GET', 'POST'])
@login_required
@admin_required
def category_add():
    form = CategoryForm()
    if form.validate_on_submit():
        try:
            category = Category(
                name=form.name.data,
                icon=form.icon.data,
                sort_order=form.sort_order.data
            )
            db.session.add(category)
            db.session.commit()
            flash(f'Kategorie "{category.name}" wurde hinzugefügt.', 'success')
            response = make_response(redirect(url_for('main.category_list')))
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response
        except Exception as e:
            db.session.rollback()
            flash('Fehler beim Erstellen der Kategorie.', 'danger')
            
    return render_template('main/category_form.html', 
                         title='Neue Kategorie',
                         form=form)

@bp.route('/admin/category/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def category_delete(id):
    category = Category.query.get_or_404(id)
    if category.articles:
        flash(f'Kategorie "{category.name}" enthält noch Artikel und kann nicht gelöscht werden.', 'danger')
    else:
        name = category.name
        db.session.delete(category)
        db.session.commit()
        flash(f'Kategorie "{name}" wurde gelöscht.', 'success')
    response = make_response(redirect(url_for('main.category_list')))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Artikel-Verwaltung
@bp.route('/admin/articles')  # URL geändert
@login_required
@admin_required
def article_list():
    categories = Category.query.order_by(Category.sort_order).all()
    return render_template('main/article_list.html', 
                         title='Artikel',
                         categories=categories)

@bp.route('/admin/article/add', methods=['GET', 'POST'])
@login_required
@admin_required
def article_add():
    form = ArticleForm()
    if request.args.get('category_id'):
        form.category_id.data = int(request.args.get('category_id'))
        
    if form.validate_on_submit():
        try:
            article = Article(
                artName=form.artName.data,
                category_id=form.category_id.data
            )
            db.session.add(article)
            db.session.commit()
            flash(f'Artikel "{article.artName}" wurde hinzugefügt.', 'success')
            # Check where the request came from to determine redirect
            referer = request.headers.get('Referer', '')
            if 'category_list' in referer:
                return redirect(url_for('main.category_list'))
            return redirect(url_for('main.article_list'))
        except Exception as e:
            db.session.rollback()
            flash('Fehler beim Erstellen des Artikels.', 'danger')
            
    return render_template('main/article_form.html', 
                         title='Neuer Artikel',
                         form=form)

@bp.route('/admin/article/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def article_edit(id):
    article = Article.query.get_or_404(id)
    form = ArticleForm(obj=article)
    
    if form.validate_on_submit():
        try:
            article.artName = form.artName.data
            article.category_id = form.category_id.data
            db.session.commit()
            flash(f'Artikel "{article.artName}" wurde aktualisiert.', 'success')
            response = make_response(redirect(url_for('main.article_list')))
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response
        except Exception as e:
            db.session.rollback()
            flash('Fehler beim Speichern des Artikels.', 'danger')
            
    return render_template('main/article_form.html', 
                         title='Artikel bearbeiten',
                         form=form)

@bp.route('/admin/article/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def article_delete(id):
    article = Article.query.get_or_404(id)
    if article.list_items:
        flash(f'Artikel "{article.artName}" wird noch in Einkaufslisten verwendet und kann nicht gelöscht werden.', 'danger')
    else:
        name = article.artName
        db.session.delete(article)
        db.session.commit()
        flash(f'Artikel "{name}" wurde gelöscht.', 'success')
    response = make_response(redirect(url_for('main.article_list')))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@bp.route('/search_articles/<search_term>')
@login_required
def search_articles(search_term):
    # Suche nach Artikeln, die den Suchbegriff enthalten (case-insensitive)
    articles = Article.query.join(Category).filter(
        Article.artName.ilike(f'%{search_term}%')
    ).all()
    
    # Wenn der aktuelle Benutzer eine aktive Einkaufsliste hat, prüfe welche Artikel bereits hinzugefügt wurden
    if current_user.is_authenticated:
        current_list_id = request.args.get('list_id')
        added_articles = set()
        if current_list_id:
            added_articles = {item.article_id for item in 
                            ShoppingListItem.query.filter_by(shopping_list_id=current_list_id).all()}
    
    # Artikel-Informationen aufbereiten
    articles_data = [{
        'id': article.id,
        'artName': article.artName,
        'category_name': article.category.name,
        'already_added': article.id in added_articles if current_user.is_authenticated else False
    } for article in articles]
    
    return jsonify({
        'articles': articles_data
    })