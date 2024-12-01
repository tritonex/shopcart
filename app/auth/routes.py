from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime, timezone
from app.auth import bp
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm
from app.extensions import db
from app.utils import admin_required

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Ungültiger Username oder falsches Passwort', 'danger')
            return redirect(url_for('auth.login'))
        
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()
        
        login_user(user, remember=form.remember_me.data)
        flash(f'Willkommen zurück, {user.username}!', 'success')
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, registered_at=datetime.now(timezone.utc))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Ihre Registrierung war erfolgreich! Sie können sich jetzt einloggen.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Registrierung', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/admin/users')  # URL geändert zu /admin/users
@login_required
@admin_required
def user_list():
    users = User.query.order_by(User.username).all()
    return render_template('auth/users.html', 
                         title='Benutzerverwaltung',
                         users=users)

@bp.route('/admin/user/<int:id>/delete', methods=['POST'])
@login_required
@admin_required

def user_delete(id):
    if current_user.id == id:
        flash('Sie können sich nicht selbst löschen!', 'danger')
        return redirect(url_for('auth.user_list'))

    user = User.query.get_or_404(id)

    if user.is_admin:
        flash('Admin-Benutzer können nicht gelöscht werden!', 'danger')
        return redirect(url_for('auth.user_list'))

    # Alle Einkaufslisten des Users löschen
    for shopping_list in user.shopping_lists:
        db.session.delete(shopping_list)

    username = user.username
    db.session.delete(user)
    db.session.commit()

    flash(f'Benutzer "{username}" wurde gelöscht.', 'success')
    return redirect(url_for('auth.user_list'))