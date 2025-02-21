from datetime import datetime
from typing import Dict, Any
from app.models.order_models import Order
from app.config import db
import random
import time

class OrderService:
    @staticmethod
    def create_order(user_id: int, items: Dict[str, Any], total_amount: float, delivery_address: Dict[str, Any]) -> Order:
        order = Order(
            user_id=user_id,
            items=items,
            total_amount=total_amount,
            delivery_address=delivery_address,
            created_at=datetime.utcnow()
        )
        db.session.add(order)
        db.session.commit()
        return order

    @staticmethod
    def process_payment() -> bool:
        """Имитация процесса оплаты с 90% вероятностью успеха"""
        time.sleep(1)  # Имитируем задержку обработки
        return random.random() < 0.9

    @staticmethod
    def get_user_orders(user_id: int, status: str = None) -> list:
        query = Order.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Order.created_at.desc()).all() 