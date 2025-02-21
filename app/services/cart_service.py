from flask import session
from app.models.product_models import Item
from typing import Tuple, Dict, Any

class CartService:
    @staticmethod
    def init_cart() -> None:
        if 'cart' not in session:
            session['cart'] = {}
            
    @staticmethod
    def get_cart_items() -> Tuple[Dict[Item, int], float]:
        total = 0
        items = {}
        
        for item_id, quantity in session.get('cart', {}).items():
            item = Item.query.get(int(item_id))
            if item:
                items[item] = quantity
                total += item.discounted_price * quantity
                
        return items, total
    
    @staticmethod
    def get_cart_total() -> float:
        total = 0
        for item_id, quantity in session.get('cart', {}).items():
            item = Item.query.get(int(item_id))
            if item:
                total += item.discounted_price * quantity
        return total

    @staticmethod
    def process_purchase() -> Tuple[bool, str]:
        cart_items, _ = CartService.get_cart_items()
        
        # Проверяем наличие товаров
        for item, quantity in cart_items.items():
            if not item.update_amount(quantity):
                return False, f"Insufficient stock for {item.title}"
                
        return True, "Purchase successful"

    @staticmethod
    def add_to_cart(item_id):
        if str(item_id) in session['cart']:
            session['cart'][str(item_id)] += 1
        else:
            session['cart'][str(item_id)] = 1
        session.modified = True

    @staticmethod
    def remove_from_cart(item_id):
        item_id = str(item_id)
        if item_id in session['cart']:
            session['cart'][item_id] -= 1
            if session['cart'][item_id] <= 0:
                del session['cart'][item_id]
            session.modified = True 