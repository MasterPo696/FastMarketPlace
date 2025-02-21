from flask import session
from app.config import db
from app.models import Item  # Update this import
from app.payments import ProcessPayment
from datetime import datetime, timedelta
from app.models.order_models import Order
import random
import time

class Basket:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def get_total_price(self):
        return sum(item.price for item in self.items)

def init_cart():
    if 'cart' not in session:
        session['cart'] = {}

def get_cart_items():
    cart_items = {}
    total = 0
    adjustments_made = False
    
    if 'cart' in session:
        for item_id, quantity in session['cart'].items():
            item = Item.query.get(int(item_id))
            if item:
                # Check if requested quantity exceeds available amount
                if quantity > item.amount:
                    session['cart'][item_id] = item.amount
                    quantity = item.amount
                    adjustments_made = True
                
                if quantity > 0:  # Only add if there's stock available
                    cart_items[item] = quantity
                    total += item.discounted_price * quantity
    
    if adjustments_made:
        session.modified = True
    
    return cart_items, total

def create_payment_form(total, secret_key, public_key):
    if total <= 0:
        return None
        
    from app.payments import ProcessPayment
    payment_processor = ProcessPayment({
        'title': 'Cart Checkout',
        'price': total
    })
    
    return payment_processor.create_payment_form({
        'amount': f"{total:.2f}",
        'currency': 'USD',
        'paymentSystem': 'Pay',
        'orderId': f"CART_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'redirect': "true"
    }, public_key)

def process_purchase():
    if 'cart' not in session:
        return False, "Empty cart"
        
    try:
        for item_id, quantity in session['cart'].items():
            item = Item.query.get(int(item_id))
            if item:
                if not item.update_amount(quantity):
                    return False, f"Insufficient stock for {item.title}"
                    
        db.session.commit()
        return True, "Purchase successful"
        
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def process_payment():
    """Имитация процесса оплаты с 90% вероятностью успеха"""
    time.sleep(1)  # Имитируем задержку обработки
    return random.random() < 0.9

def create_order(user_id, items, total_amount, delivery_address):
    """
    Создает новый заказ
    
    Args:
        user_id: ID пользователя
        items: словарь с информацией о товарах
        total_amount: общая сумма заказа
        delivery_address: словарь с адресом доставки
    """
    order = Order(
        user_id=user_id,
        items=items,
        total_amount=total_amount,
        delivery_address=delivery_address,  # delivery_address уже является словарем
        created_at=datetime.utcnow()
    )
    db.session.add(order)
    db.session.commit()
    return order
    
    
