from flask import session
from app.config import db
from app.models import Item  # Update this import
from app.payments import ProcessPayment
from datetime import datetime

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
    
    if 'cart' in session:
        for item_id, quantity in session['cart'].items():
            item = Item.query.get(int(item_id))
            if item:
                cart_items[item] = quantity
                total += item.discounted_price * quantity
    
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
    
    
