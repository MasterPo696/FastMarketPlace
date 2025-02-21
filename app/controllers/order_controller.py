from flask import render_template, jsonify
from app.auth import get_current_user, login_required
from app.models.order_models import Order
from app.config import db, app
from datetime import datetime, timedelta

class OrderController:
    @staticmethod
    @login_required
    def show_orders():
        """Display user's orders"""
        try:
            user_id = get_current_user().id
            
            # Получаем все заказы пользователя
            orders = Order.query.filter_by(user_id=user_id).all()
            
            # Обновляем статусы заказов
            for order in orders:
                if order.update_status():
                    db.session.add(order)
            
            if db.session.dirty:
                db.session.commit()
            
            # Получаем обновленные списки заказов
            active_orders = Order.query.filter_by(
                user_id=user_id,
                status='active'
            ).order_by(Order.created_at.desc()).all()
            
            completed_orders = Order.query.filter_by(
                user_id=user_id,
                status='completed'
            ).order_by(Order.completed_at.desc()).all()
            
            return render_template(
                'orders.html',
                active_orders=active_orders,
                completed_orders=completed_orders
            )
        except Exception as e:
            app.logger.error(f"Error showing orders: {str(e)}")
            return jsonify({'error': 'Failed to load orders'}), 500

    @staticmethod
    def has_active_orders():
        """Check if user has active orders"""
        try:
            if get_current_user():
                active_orders = Order.query.filter_by(
                    user_id=get_current_user().id,
                    status='active'
                ).count()
                return active_orders > 0
            return False
        except Exception as e:
            app.logger.error(f"Error checking active orders: {str(e)}")
            return False 