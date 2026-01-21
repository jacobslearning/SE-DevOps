from flask import session, flash, redirect, url_for
from functools import wraps
from models import User 

def current_user():
    """Get current logged in user"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

def login_required(f):
    """If login is required to access route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """If Admin role required to access route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = current_user()
        if not user or user.role != 'Admin':
            flash("Unauthorized Access", "danger")
            return redirect(url_for('dashboard.dashboard'))
        return f(*args, **kwargs)
    return decorated_function