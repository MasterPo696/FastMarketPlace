from flask import render_template, request, redirect, session, flash, url_for
from app.models.user_models import User
from app.auth import send_verification_code, get_current_user
from app.config import db
from datetime import datetime

class AuthController:
    @staticmethod
    def login():
        if request.method == 'POST':
            identifier = request.form.get('identifier')
            password = request.form.get('password')
            remember = request.form.get('remember', False)
            
            user = User.query.filter(
                (User.email == identifier) | (User.phone == identifier)
            ).first()
            
            if user and user.check_password(password):
                if not user.is_active:
                    flash('Please verify your account first', 'warning')
                    return redirect(url_for('verify', user_id=user.id))
                    
                session['user_id'] = user.id
                
                if remember:
                    user.generate_auth_token()
                    db.session.commit()
                    
                    response = redirect(request.args.get('next') or '/')
                    response.set_cookie('remember_token', user.auth_token, 
                                     max_age=30*24*60*60, httponly=True)
                    return response
                    
                return redirect(request.args.get('next') or '/')
                
            flash('Invalid credentials', 'error')
        
        return render_template('auth/login.html')

    @staticmethod
    def register():
        if request.method == 'POST':
            name = request.form.get('name')
            identifier = request.form.get('identifier')
            password = request.form.get('password')
            
            is_email = '@' in identifier
            
            existing_user = User.query.filter(
                (User.email == identifier if is_email else User.phone == identifier)
            ).first()
            
            if existing_user:
                flash('User already exists', 'error')
                return redirect(url_for('login'))
                
            user = User(
                name=name,
                email=identifier if is_email else None,
                phone=identifier if not is_email else None,
                is_active=False
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            send_verification_code(user)
            
            return redirect(url_for('verify', user_id=user.id))
            
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
        session.pop('user_id', None)
        response = redirect('/')
        response.delete_cookie('remember_token')
        return response 