from flask import render_template, request, redirect, session, flash, url_for
from app.models.user_models import User
from app.auth import send_verification_code, get_current_user
from app.config import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class AuthController:
    @staticmethod
    def login():
        """Handle user login"""
        if request.method == 'POST':
            identifier = request.form.get('identifier')
            password = request.form.get('password')
            
            # Ищем пользователя только по email
            user = User.query.filter_by(email=identifier).first()
            
            if user and user.check_password(password):
                session['user_id'] = user.id
                session.permanent = True
                flash('Successfully logged in!', 'success')
                return redirect(url_for('index'))
            
            flash('Invalid email or password', 'error')
            
        return render_template('auth/login.html')

    @staticmethod
    def register():
        """Handle user registration"""
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return redirect(url_for('register'))
            
            user = User(email=email)
            user.set_password(password)
            
            try:
                db.session.add(user)
                db.session.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash('Registration failed. Please try again.', 'error')
                
        return render_template('auth/register.html')

    @staticmethod
    def verify(user_id):
        user = User.query.get_or_404(user_id)
        
        if request.method == 'POST':
            code = request.form.get('code')
            
            if (user.verification_code == code and 
                datetime.now() < user.code_expiry):
                user.is_active = True
                user.verification_code = None
                db.session.commit()
                
                session['user_id'] = user.id
                flash('Account verified successfully!', 'success')
                return redirect('/')
                
            flash('Invalid or expired code', 'error')
            
        return render_template('auth/verify.html', user=user)

    @staticmethod
    def logout():
        """Handle user logout"""
        session.pop('user_id', None)
        flash('Successfully logged out!', 'success')
        return redirect(url_for('index')) 