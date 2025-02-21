from flask import render_template, session, jsonify, redirect, url_for, request, flash, render_template_string
from app.services.cart_service import CartService
from app.auth import get_current_user, login_required
from datetime import datetime
from app.config import db, app

class CartController:
    @staticmethod
    def show_cart():
        """Display cart page"""
        try:
            CartService.init_cart()
            cart_items, total = CartService.get_cart_items()
            return render_template(
                "cart.html", 
                cart_items=cart_items, 
                total=total,
                datetime=datetime
            )
        except Exception as e:
            app.logger.error(f"Error showing cart: {str(e)}")
            flash('Error loading cart. Please try again.', 'error')
            return redirect(url_for('index'))

    @staticmethod
    def add_to_cart(item_id):
        """Add item to cart"""
        try:
            CartService.init_cart()
            CartService.add_to_cart(item_id)
            
            cart_items, total = CartService.get_cart_items()
            
            # Рендерим HTML для корзины
            if cart_items:
                cart_html = render_template_string("""
                    {% for item, quantity in cart_items.items() %}
                    <div class="cart-item">
                        <div class="d-flex align-items-center mb-2">
                            <img src="{{ url_for('static', filename=item.image_path) }}" alt="{{ item.title }}">
                            <div class="ms-3 flex-grow-1">
                                <h6 class="mb-0">{{ item.title }}</h6>
                                <small class="text-muted">{{ item.weight }} г</small>
                                <div class="mt-1">
                                    <small class="text-muted d-block">
                                        Категория: {{ item.subcategory.category.name }}
                                    </small>
                                    <small class="text-muted d-block">
                                        В наличии: {{ item.amount }} шт
                                    </small>
                                </div>
                                <div class="d-flex justify-content-between align-items-center mt-2">
                                    <span class="fw-bold">${{ "%.2f"|format(item.discounted_price) }}</span>
                                    <div class="btn-group btn-group-sm">
                                        <button onclick="removeFromCart({{ item.id }})" class="btn btn-outline-secondary">-</button>
                                        <span class="btn btn-outline-secondary disabled">{{ quantity }}</span>
                                        <button onclick="addToCart({{ item.id }})" class="btn btn-outline-secondary">+</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                """, cart_items=cart_items)
            else:
                cart_html = """
                    <div class="text-center py-5">
                        <p class="text-muted">Корзина пуста</p>
                    </div>
                """
            
            return jsonify({
                'success': True,
                'cart_count': sum(cart_items.values()),
                'cart_total': total,
                'cart_html': cart_html
            })
        except Exception as e:
            app.logger.error(f"Error adding to cart: {str(e)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'error': 'Error adding to cart'})
            flash('Error adding item to cart. Please try again.', 'error')
            return redirect(request.referrer or url_for('index'))

    @staticmethod
    def remove_from_cart(item_id):
        """Remove item from cart"""
        try:
            CartService.remove_from_cart(item_id)
            cart_items, total = CartService.get_cart_items()
            
            # Рендерим HTML для корзины
            cart_html = render_template_string("""
                {% for item, quantity in cart_items.items() %}
                <div class="cart-item">
                    <div class="d-flex align-items-center mb-2">
                        <img src="{{ url_for('static', filename=item.image_path) }}" alt="{{ item.title }}">
                        <div class="ms-3 flex-grow-1">
                            <h6 class="mb-0">{{ item.title }}</h6>
                            <small class="text-muted">{{ item.weight }} г</small>
                            <div class="mt-1">
                                <small class="text-muted d-block">
                                    Категория: {{ item.subcategory.category.name }}
                                </small>
                                <small class="text-muted d-block">
                                    В наличии: {{ item.amount }} шт
                                </small>
                            </div>
                            <div class="d-flex justify-content-between align-items-center mt-2">
                                <span class="fw-bold">${{ "%.2f"|format(item.discounted_price) }}</span>
                                <div class="btn-group btn-group-sm">
                                    <button onclick="removeFromCart({{ item.id }})" class="btn btn-outline-secondary">-</button>
                                    <span class="btn btn-outline-secondary disabled">{{ quantity }}</span>
                                    <button onclick="addToCart({{ item.id }})" class="btn btn-outline-secondary">+</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            """, cart_items=cart_items)
            
            return jsonify({
                'success': True,
                'cart_count': sum(cart_items.values()),
                'cart_total': total,
                'cart_html': cart_html
            })
        except Exception as e:
            app.logger.error(f"Error removing from cart: {str(e)}")
            flash('Error removing item from cart. Please try again.', 'error')
            return redirect(request.referrer or url_for('index'))

    @staticmethod
    def get_cart_items_json():
        """Get cart items in JSON format"""
        try:
            cart_items, total = CartService.get_cart_items()
            items_json = [{
                'id': item.id,
                'title': item.title,
                'price': item.discounted_price,
                'quantity': quantity,
                'image_path': url_for('static', filename=item.image_path) if item.image_path else ''
            } for item, quantity in cart_items.items()]
            
            return jsonify({
                'items': items_json,
                'total': f"{total:.2f}"
            })
        except Exception as e:
            app.logger.error(f"Error getting cart items JSON: {str(e)}")
            return jsonify({'error': 'Error loading cart items'})

    @staticmethod
    @login_required
    def process_order():
        try:
            from app.services.order_service import OrderService
            
            if OrderService.process_payment():
                cart_items, total = CartService.get_cart_items()
                user = get_current_user()
                
                if not user:
                    return jsonify({'success': False, 'error': 'User not found'})
                
                if not user.address:
                    return jsonify({'success': False, 'error': 'Delivery address required'})
                
                order = OrderService.create_order(
                    user_id=user.id,
                    items={str(item.id): {
                        'title': item.title,
                        'quantity': quantity,
                        'price': item.discounted_price
                    } for item, quantity in cart_items.items()},
                    total_amount=total,
                    delivery_address=user.address
                )
                
                success, message = CartService.process_purchase()
                if not success:
                    db.session.delete(order)
                    db.session.commit()
                    return jsonify({'success': False, 'error': message})
                
                session['cart'] = {}
                session.modified = True
                
                return jsonify({
                    'success': True,
                    'order_id': order.id
                })
            
            return jsonify({
                'success': False,
                'error': 'Payment failed. Please try again.'
            })
            
        except Exception as e:
            app.logger.error(f"Error processing order: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'An error occurred while processing your order.'
            }) 