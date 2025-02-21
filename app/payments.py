import hashlib
from datetime import datetime
import logging
from flask import render_template
from toml import load

# Загружаем ключи из конфигурационного файла
config = load('secrets/config.toml')
PUBLIC = config['public']
SECRET = config['secret']

class ProcessPayment:
    def __init__(self, item):
        self.item = item

    def create_payment_form(self, params, public_key):
        url = f"https://merchant.betatransfer.io/api/payment?token={public_key}"
        
        form = f'<form class="merchant" action="{url}" method="post">'
        for key, value in params.items():
            form += f'<input type="hidden" name="{key}" value="{value}">'
        form += '<button type="submit" class="btn btn-primary">Proceed to Payment</button>'
        form += '</form>'
        
        return form

    def generate_signature(self, data, secret):
        # Для стабильности сортируем ключи по алфавиту
        sorted_items = [str(data[key]) for key in sorted(data.keys())]
        # Если параметр redirect должен быть строкой, можно принудительно преобразовать его:
        # sorted_items = [str(data[key]).lower() if key == 'redirect' else str(data[key]) for key in sorted(data.keys())]
        values = ''.join(sorted_items) + secret
        return hashlib.md5(values.encode()).hexdigest()

    def process_payment(self, id):
        try:
            order_id = f"ORDER_{id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Форматируем цену с двумя десятичными знаками (если требуется)
            amount_str = f"{self.item.price:.2f}"
            
            payment_data = {
                'amount': amount_str,
                'currency': 'USD', 
                'paymentSystem': 'Pay',
                'orderId': order_id,
                # Приводим redirect к строке, чтобы соответствовать тому, что ожидает API (если нужно)
                'redirect': "true"
            }

            payment_data['sign'] = self.generate_signature(payment_data, SECRET)
            form_html = self.create_payment_form(payment_data, PUBLIC)

            return render_template(
                "payment.html",
                item=self.item,
                form=form_html
            )
        except Exception as e:
            logging.error(f"Payment processing error: {str(e)}")
            raise