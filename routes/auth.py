from flask import (
    Blueprint, render_template, request, flash, url_for, redirect, session
)
from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from routes.utils import log_action, login_required
from database import db
from models import User

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = 'User'

        if not username or not password:
            flash('Username and password are required.', 'danger')
        elif User.query.filter_by(username=username).first():
            flash('Username is already taken.', 'danger')
        else:
            password_hash = generate_password_hash(password)
            new_user = User(
                username=username,
                password_hash=password_hash,
                role=role
            )
            db.session.add(new_user)
            db.session.commit()
            log_action(
                new_user.id,
                f"Registered account as {username} (ID: {new_user.id})"
            )
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('Incorrect username.', 'danger')
        elif not check_password_hash(user.password_hash, password):
            flash('Incorrect password.', 'danger')
        else:
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            log_action(user.id, f"Logged in as {username} (ID: {user.id})")
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('dashboard.dashboard'))

    return render_template('login.html')


@auth_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    log_action(
        session['user_id'],
        f"Logged out as {session['username']} (ID: {session['user_id']})"
    )
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))