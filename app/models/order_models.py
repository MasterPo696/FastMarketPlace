from app.config import db
from datetime import datetime, timedelta

class Order(db.Model):
    __bind_key__ = 'orders'  # Используем отдельную БД для заказов
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    items = db.Column(db.JSON, nullable=False)  # Хранит список товаров и их количество
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    delivery_address = db.Column(db.JSON, nullable=True)

    @property
    def is_expired(self):
        """Check if order is expired (older than 30 minutes)"""
        if not self.created_at:
            return False
        return datetime.utcnow() - self.created_at > timedelta(minutes=30)

    def update_status(self):
        """Update order status based on time"""
        if self.status == 'active' and self.is_expired:
            self.status = 'completed'
            self.completed_at = datetime.utcnow()
            return True
        return False 