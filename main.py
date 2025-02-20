from flask import render_template, request, redirect, session, jsonify
from toml import load
from app.payments import ProcessPayment
from app.pictures import ImageHandler
from app.config import app, db

# Добавим секретный ключ для работы с сессиями
app.secret_key = 'your-secret-key-here'  # Замените на свой секретный ключ

class Item(db.Model):

    # Основные данные
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Цена и скидка
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float(100), nullable=False)

    # Количество и доступность
    amount = db.Column(db.Integer, nullable=False)
    isAvailable = db.Column(db.Boolean, default=True)
    
    image_path = db.Column(db.String(200))

    def __repr__(self):
        return f'{self.title}'

@app.route('/')
def index():
    if 'cart' not in session:
        session['cart'] = []
    items = Item.query.order_by(Item.price).all()
    return render_template("index.html", data=items)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/buy/<int:id>')
def buy(id):
    try:
        item = Item.query.get_or_404(id)
        payment_processor = ProcessPayment(item)
        return payment_processor.process_payment(id)
    except Exception as e:
        app.logger.error(f"Payment error: {str(e)}")
        return "Payment error occurred", 500

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']
        
        if 'image' not in request.files:
            return "No image file provided", 400
        
        image_handler = ImageHandler()
        image_path, error, code = image_handler.handle_image_upload(request.files['image'])
        if error:
            return error, code

        item = Item(
            title=title,
            price=price,
            description=description,
            image_path=image_path
        )

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error adding item to database: {str(e)}", 500
    else:
        return render_template("create.html")

@app.route('/update_cart/<int:id>/<action>', methods=['POST'])
def update_cart(id, action):
    if 'cart' not in session:
        session['cart'] = []
    
    cart = session['cart']
    
    if action == 'add':
        cart.append(id)
    elif action == 'remove' and id in cart:
        cart.remove(id)
    elif action == 'delete':
        cart = [item for item in cart if item != id]
    
    session['cart'] = cart
    
    return jsonify({
        'count': cart.count(id),
        'total_items': len(cart)
    })

@app.route('/cart')
def cart():
    if 'cart' not in session:
        session['cart'] = []
    
    cart_items = []
    total_price = 0
    
    # Получаем уникальные ID товаров из корзины
    unique_ids = set(session['cart'])
    
    # Получаем информацию о каждом товаре
    for id in unique_ids:
        item = Item.query.get(id)
        if item:
            cart_items.append(item)
            total_price += item.price * session['cart'].count(id)
    
    return render_template(
        'cart.html',
        cart_items=cart_items,
        total_price=total_price
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)