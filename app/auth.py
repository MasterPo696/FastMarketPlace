from functools import wraps
from flask import session, redirect, url_for, flash, request
from datetime import datetime, timedelta
import secrets
from app.models import User
from app.config import db

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    
    # Check for remember token in cookie
    token = request.cookies.get('remember_token')
    if token:
        user = User.query.filter_by(auth_token=token).first()
        if user and user.is_token_valid():
            session['user_id'] = user.id
            return user
    return None

def send_verification_code(user):
    # In production, implement actual email/SMS sending
    # For now, just set a fixed code
    user.verification_code = "12345"
    user.code_expiry = datetime.now() + timedelta(minutes=15)
    db.session.commit()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or not user.is_admin:
            flash('Access denied. Admin rights required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function 