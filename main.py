from flask import render_template, request, redirect, session, jsonify
from toml import load
from app.payments import ProcessPayment
from app.config import app, db
from app.cart import init_cart, get_cart_items, create_payment_form
from app.creation import handle_item_creation, get_categories, get_subcategories
from datetime import datetime
from app.models import Item, Category, Subcategory
import json

# Load config
config = load('secrets/config.toml')
PUBLIC = config['public']
SECRET = config['secret']

# Routes
@app.route('/')
def index():
    init_cart()
    category_id = request.args.get('category_id', type=int)
    subcategory_id = request.args.get('subcategory_id', type=int)
    
    # Получаем все категории для навигации
    categories = Category.query.all()
    
    # Фильтруем товары
    query = Item.query
    if subcategory_id:
        query = query.filter_by(subcategory_id=subcategory_id)
    elif category_id:
        query = query.join(Subcategory).filter(Subcategory.category_id == category_id)
    
    items = query.order_by(Item.price).all()
    
    return render_template(
        "index.html",
        data=items,
        categories=categories,
        current_category_id=category_id,
        current_subcategory_id=subcategory_id
    )

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
        if 'image' not in request.files:
            return "No image file provided", 400
            
        error, code = handle_item_creation(request.form, request.files['image'])
        if error:
            return error, code
        return redirect('/')
    
    categories = get_categories()
    return render_template("create.html", categories=categories)

@app.route('/get_subcategories/<int:category_id>')
def get_subcategories_route(category_id):
    subcategories = get_subcategories(category_id)
    return jsonify([{'id': s.id, 'name': s.name} for s in subcategories])

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    init_cart()
    
    item_id = str(id)
    if item_id in session['cart']:
        session['cart'][item_id] += 1
    else:
        session['cart'][item_id] = 1
    
    session.modified = True
    return redirect(request.referrer or '/')

@app.route('/remove_from_cart/<int:id>')
def remove_from_cart(id):
    item_id = str(id)
    if 'cart' in session and item_id in session['cart']:
        session['cart'][item_id] -= 1
        if session['cart'][item_id] <= 0:
            del session['cart'][item_id]
        session.modified = True
    return redirect(request.referrer or '/')

@app.route('/cart')
def cart():
    init_cart()
    cart_items, total = get_cart_items()
    payment_form = create_payment_form(total, SECRET, PUBLIC) if cart_items else None

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total,
        payment_form=payment_form
    )

@app.route('/checkout', methods=['GET'])
def checkout():
    init_cart()
    cart_items, total = get_cart_items()
    
    if not cart_items:
        return redirect('/')
        
    try:
        payment_processor = ProcessPayment({
            'title': 'Cart Checkout',
            'price': total
        })
        
        payment_form = payment_processor.create_payment_form({
            'amount': f"{total:.2f}",
            'currency': 'USD',
            'paymentSystem': 'Pay',
            'orderId': f"CART_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'redirect': "true"
        }, PUBLIC)
        
        return render_template(
            "cart.html",
            cart_items=cart_items,
            total=total,
            payment_form=payment_form
        )
    except Exception as e:
        app.logger.error(f"Checkout error: {str(e)}")
        return "Error processing checkout", 500

def init_categories():
    if Category.query.first() is None:
        with open('app/categories.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for cat_data in data['categories']:
            category = Category(name=cat_data['name'])
            db.session.add(category)
            db.session.flush()  # Получаем ID категории
            
            for subcat_name in cat_data['subcategories']:
                subcategory = Subcategory(
                    name=subcat_name,
                    category_id=category.id
                )
                db.session.add(subcategory)
        
        db.session.commit()

def get_categories():
    return Category.query.all()

def get_subcategories(category_id):
    return Subcategory.query.filter_by(category_id=category_id).all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_categories()
    app.run(debug=True)