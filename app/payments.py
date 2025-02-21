import hashlib
from datetime import datetime
import logging
from flask import render_template
import random
import time
from app.models import Receipt
from app.config import db
from flask import session

class ProcessPayment:
    def __init__(self, item):
        self.item = item

    def create_payment_form(self, params, public_key):
        form = '''
            <form class="payment-form" id="paymentForm" method="POST" action="/process_payment">
                <div class="mb-4">
                    <label class="form-label fw-medium">Card Number</label>
                    <input type="text" 
                           class="form-control form-control-lg" 
                           name="card_number"
                           id="cardNumber" 
                           required 
                           maxlength="19"
                           oninput="formatCardNumber(this)"
                           placeholder="0000 0000 0000 0000">
                </div>
                
                <div class="mb-4">
                    <label class="form-label fw-medium">Cardholder Name</label>
                    <input type="text" 
                           class="form-control form-control-lg" 
                           name="cardholder_name"
                           id="cardName" 
                           required
                           placeholder="JOHN DOE">
                </div>
                
                <div class="row mb-4">
                    <div class="col">
                        <label class="form-label fw-medium">Expiry Date</label>
                        <input type="text" 
                               class="form-control form-control-lg" 
                               name="expiry"
                               id="expiry" 
                               required
                               maxlength="5"
                               oninput="formatExpiry(this)"
                               placeholder="MM/YY">
                    </div>
                    <div class="col">
                        <label class="form-label fw-medium">CVV</label>
                        <input type="password" 
                               class="form-control form-control-lg" 
                               name="cvv"
                               id="cvv" 
                               required
                               maxlength="3"
                               placeholder="•••">
                    </div>
                </div>

                <input type="hidden" name="order_id" value="''' + params['orderId'] + '''">
                <input type="hidden" name="amount" value="''' + params['amount'] + '''">

                <div id="paymentStatus" class="alert d-none mb-4"></div>
                
                <button type="submit" class="btn btn-primary btn-lg w-100 position-relative" id="payButton">
                    <span class="payment-button-text">Pay $''' + params['amount'] + '''</span>
                    <span class="payment-button-loader d-none">
                        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        Processing...
                    </span>
                </button>
            </form>
            
            <style>
                .payment-form .form-control {
                    border: 1.5px solid #dee2e6;
                    padding: 0.75rem 1rem;
                    font-size: 1rem;
                    border-radius: 12px;
                    background-color: #fff;
                    transition: all 0.2s ease-in-out;
                }
                
                .payment-form .form-control:focus {
                    border-color: #0d6efd;
                    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.15);
                }
                
                .payment-form .btn-primary {
                    padding: 1rem;
                    font-weight: 500;
                    border-radius: 12px;
                    transition: all 0.2s ease-in-out;
                }
                
                .payment-form .btn-primary:hover {
                    transform: translateY(-1px);
                    box-shadow: 0 4px 12px rgba(13, 110, 253, 0.15);
                }
                
                .payment-form .alert {
                    border-radius: 12px;
                    font-weight: 500;
                }
                
                [data-bs-theme="dark"] .payment-form .form-control {
                    background-color: #2b3035;
                    border-color: #495057;
                }
                
                [data-bs-theme="dark"] .payment-form .form-control:focus {
                    border-color: #0d6efd;
                }
            </style>

            <script>
                function formatCardNumber(input) {
                    let value = input.value.replace(/\D/g, '');
                    let formattedValue = '';
                    
                    for (let i = 0; i < value.length; i++) {
                        if (i > 0 && i % 4 === 0) {
                            formattedValue += ' ';
                        }
                        formattedValue += value[i];
                    }
                    
                    input.value = formattedValue;
                }

                function formatExpiry(input) {
                    let value = input.value.replace(/\D/g, '');
                    if (value.length >= 2) {
                        value = value.slice(0,2) + '/' + value.slice(2);
                    }
                    input.value = value;
                }

                document.getElementById('paymentForm').addEventListener('submit', function(event) {
                    event.preventDefault();
                    
                    const button = document.getElementById('payButton');
                    const buttonText = button.querySelector('.payment-button-text');
                    const buttonLoader = button.querySelector('.payment-button-loader');
                    const status = document.getElementById('paymentStatus');
                    
                    button.disabled = true;
                    buttonText.classList.add('d-none');
                    buttonLoader.classList.remove('d-none');
                    
                    status.className = 'alert alert-info';
                    status.classList.remove('d-none');
                    status.textContent = 'Processing payment...';

                    setTimeout(() => {
                        const success = Math.random() > 0.1;
                        
                        if (success) {
                            status.className = 'alert alert-success';
                            status.textContent = 'Payment successful! Redirecting...';
                            this.submit();
                        } else {
                            status.className = 'alert alert-danger';
                            status.textContent = 'Payment failed. Please try again.';
                            button.disabled = false;
                            buttonText.classList.remove('d-none');
                            buttonLoader.classList.add('d-none');
                        }
                    }, 2000);
                });
            </script>
        '''
        return form

    def process_payment(self, id):
        try:
            order_id = f"ORDER_{id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            amount_str = f"{self.item.price:.2f}"
            
            payment_data = {
                'amount': amount_str,
                'currency': 'USD',
                'orderId': order_id,
            }

            return render_template(
                "payment.html",
                item=self.item,
                form=self.create_payment_form(payment_data, '')
            )
        except Exception as e:
            logging.error(f"Payment processing error: {str(e)}")
            raise


# class ProcessPayment:
#     def __init__(self, item):
#         self.item = item

#     def create_payment_form(self, params, public_key):
#         url = f"https://merchant.betatransfer.io/api/payment?token={public_key}"
        
#         form = f'<form class="merchant" action="{url}" method="post">'
#         for key, value in params.items():
#             form += f'<input type="hidden" name="{key}" value="{value}">'
#         form += '<button type="submit" class="btn btn-primary">Proceed to Payment</button>'
#         form += '</form>'
        
#         return form

#     def generate_signature(self, data, secret):
#         # Для стабильности сортируем ключи по алфавиту
#         sorted_items = [str(data[key]) for key in sorted(data.keys())]
#         # Если параметр redirect должен быть строкой, можно принудительно преобразовать его:
#         # sorted_items = [str(data[key]).lower() if key == 'redirect' else str(data[key]) for key in sorted(data.keys())]
#         values = ''.join(sorted_items) + secret
#         return hashlib.md5(values.encode()).hexdigest()

#     def process_payment(self, id):
#         try:
#             order_id = f"ORDER_{id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
#             # Форматируем цену с двумя десятичными знаками (если требуется)
#             amount_str = f"{self.item.price:.2f}"
            
#             payment_data = {
#                 'amount': amount_str,
#                 'currency': 'USD', 
#                 'paymentSystem': 'Pay',
#                 'orderId': order_id,
#                 # Приводим redirect к строке, чтобы соответствовать тому, что ожидает API (если нужно)
#                 'redirect': "true"
#             }

#             payment_data['sign'] = self.generate_signature(payment_data, SECRET)
#             form_html = self.create_payment_form(payment_data, PUBLIC)

#             return render_template(
#                 "payment.html",
#                 item=self.item,
#                 form=form_html
#             )
#         except Exception as e:
#             logging.error(f"Payment processing error: {str(e)}")
#             raise
