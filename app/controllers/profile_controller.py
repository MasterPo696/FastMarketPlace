from flask import render_template
from app.auth import login_required, get_current_user
from app.models.user_models import Receipt
from app.models.order_models import Order
from datetime import datetime, timedelta

class ProfileController:
    @staticmethod
    @login_required
    def show_profile():
        """Display user profile page"""
        user = get_current_user()
        
        # Get recent orders (last 30 days)
        recent_orders = Order.query.filter_by(
            user_id=user.id
        ).filter(
            Order.created_at >= datetime.utcnow() - timedelta(days=30)
        ).order_by(
            Order.created_at.desc()
        ).limit(5).all()
        
        # Get recent receipts
        receipts = Receipt.query.filter_by(
            user_id=user.id
        ).order_by(
            Receipt.purchase_date.desc()
        ).limit(5).all()
            
        return render_template(
            'auth/profile.html', 
            user=user,
            recent_orders=recent_orders,
            receipts=receipts
        )

    @staticmethod
    @login_required
    def show_settings():
        """Display user settings page"""
        user = get_current_user()
        return render_template('auth/settings.html', user=user) 