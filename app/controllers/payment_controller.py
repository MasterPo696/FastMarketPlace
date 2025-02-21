from flask import request, redirect, flash, url_for
from app.models.product_models import Item
from app.models.user_models import Receipt
from app.models.order_models import Order
from app.payments import ProcessPayment
from app.cart import get_cart_items, process_purchase
from app.auth import get_current_user
from app.config import db, app
from datetime import datetime

class PaymentController:
    @staticmethod
    def buy(id):
        try:
            item = Item.query.get_or_404(id)
            payment_processor = ProcessPayment(item)
            return payment_processor.process_payment(id)
        except Exception as e:
            app.logger.error(f"Payment error: {str(e)}")
            return "Payment error occurred", 500

    @staticmethod
    def process_payment():
        try:
            # Get payment details
            card_number = request.form['card_number']
            cardholder_name = request.form['cardholder_name']
            order_id = request.form['order_id']
            amount = float(request.form['amount'])
            
            # Get current user
            current_user = get_current_user()
            
            # Get cart items for receipt
            cart_items, _ = get_cart_items()
            items_data = {
                str(item.id): {
                    'title': item.title,
                    'price': item.discounted_price,
                    'quantity': quantity
                } for item, quantity in cart_items.items()
            }
            
            # Create receipt
            receipt = Receipt(
                order_id=order_id,
                card_number=card_number,
                cardholder_name=cardholder_name,
                total_amount=amount,
                purchase_date=datetime.now(),
                items=items_data,
                user_id=current_user.id if current_user else None
            )
            
            # Process purchase (update inventory)
            success, message = process_purchase()
            
            if success:
                # Save receipt
                db.session.add(receipt)
                db.session.commit()
                
                # Clear cart
                session['cart'] = {}
                session.modified = True
                
                flash('Payment successful! Thank you for your purchase.', 'success')
                return redirect('/')
            else:
                flash(f'Payment failed: {message}', 'error')
                return redirect('/cart')
                
        except Exception as e:
            app.logger.error(f"Payment processing error: {str(e)}")
            flash('An error occurred while processing your payment.', 'error')
            return redirect('/cart') 