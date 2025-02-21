from flask import render_template
from app.auth import get_current_user, login_required
from app.models.order_models import Order

class OrderController:
    @staticmethod
    @login_required
    def show_orders():
        """Display user's orders"""
        active_orders = Order.query.filter_by(
            user_id=get_current_user().id,
            status='active'
        ).order_by(Order.created_at.desc()).all()
        
        completed_orders = Order.query.filter_by(
            user_id=get_current_user().id,
            status='completed'
        ).order_by(Order.completed_at.desc()).all()
        
        return render_template(
            'orders.html',
            active_orders=active_orders,
            completed_orders=completed_orders
        )

    @staticmethod
    def has_active_orders():
        """Check if user has active orders"""
        if get_current_user():
            active_orders = Order.query.filter_by(
                user_id=get_current_user().id,
                status='active'
            ).count()
            return active_orders > 0
        return False 