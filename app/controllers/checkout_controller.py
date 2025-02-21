from flask import render_template, request, redirect, flash
from app.services.cart_service import CartService
from app.auth import get_current_user
from app.config import app

class CheckoutController:
    @staticmethod
    def show_checkout():
        """Display checkout page"""
        CartService.init_cart()
        
        if request.method == 'POST':
            user = get_current_user()
            if not user or not user.address:
                flash('Please add delivery address first', 'warning')
                return redirect('/cart')
                
            success, message = CartService.process_purchase()
            if success:
                return redirect('/')
            else:
                flash(message, 'error')
                return redirect('/cart')
        
        cart_items, total = CartService.get_cart_items()
        
        if not cart_items:
            return redirect('/')
            
        try:
            user = get_current_user()
            has_address = user and user.address
            
            payment_form = CheckoutController._generate_payment_form(user, has_address)
            
            return render_template(
                "cart.html",
                cart_items=cart_items,
                total=total,
                payment_form=payment_form
            )
        except Exception as e:
            app.logger.error(f"Checkout error: {str(e)}")
            return "Error processing checkout", 500

    @staticmethod
    def _generate_payment_form(user, has_address):
        """Generate payment form HTML"""
        return f"""
            <div class="mb-4">
                <h5>Delivery Address</h5>
                {user.address['address'] if has_address else '<p class="text-muted">No address set</p>'}
                <button type="button" class="btn btn-outline-primary mt-2" 
                        data-bs-toggle="modal" data-bs-target="#addressModal">
                    {'Edit Address' if has_address else 'Add Address'}
                </button>
            </div>
            <form method="post" action="/checkout">
                <button type="submit" class="btn btn-primary w-100" 
                        {'disabled' if not has_address else ''}>
                    Complete Purchase (Demo)
                </button>
            </form>
        """ 