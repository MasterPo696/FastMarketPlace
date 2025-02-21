from flask import render_template
from app.config import app
from app.cart import init_cart
from app.auth import login_required, admin_required
from datetime import datetime
from app.controllers.product_controller import ProductController
from app.controllers.payment_controller import PaymentController
from app.controllers.category_controller import CategoryController
from app.controllers.cart_controller import CartController
from app.controllers.address_controller import AddressController
from app.controllers.checkout_controller import CheckoutController
from app.controllers.auth_controller import AuthController
from app.controllers.profile_controller import ProfileController
from app.controllers.map_controller import MapController
from app.controllers.order_controller import OrderController

def register_routes():
    # Basic routes
    @app.route('/')
    def index():
        init_cart()
        return ProductController.index()

    @app.route('/about')
    def about():
        return render_template("about.html")

    # Product routes
    @app.route('/buy/<int:id>')
    def buy(id):
        return PaymentController.buy(id)

    @app.route('/get_subcategories/<int:category_id>')
    def get_subcategories_route(category_id):
        return CategoryController.get_subcategories(category_id)

    # Cart routes
    @app.route('/add_to_cart/<int:id>')
    def add_to_cart(id):
        return CartController.add_to_cart(id)

    @app.route('/remove_from_cart/<int:id>')
    def remove_from_cart(id):
        return CartController.remove_from_cart(id)

    @app.route('/cart')
    def cart():
        return CartController.show_cart()

    @app.route('/process_order', methods=['POST'])
    @login_required
    def process_order():
        return CartController.process_order()

    # Address routes
    @app.route('/save_address', methods=['POST'])
    @login_required
    def save_address():
        return AddressController.save_address()

    # Checkout routes
    @app.route('/checkout', methods=['GET', 'POST'])
    def checkout():
        return CheckoutController.show_checkout()

    # Payment routes
    @app.route('/process_payment', methods=['POST'])
    def process_payment():
        return PaymentController.process_payment()

    @app.route('/get_cart_items')
    def get_cart_items_json():
        return CartController.get_cart_items_json()

    # User routes
    @app.route('/profile')
    @login_required
    def profile():
        return ProfileController.show_profile()

    @app.route('/orders')
    @login_required
    def orders():
        return OrderController.show_orders()

    # Auth routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return AuthController.login()

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        return AuthController.register()

    @app.route('/verify/<int:user_id>', methods=['GET', 'POST'])
    def verify(user_id):
        return AuthController.verify(user_id)

    @app.route('/logout')
    def logout():
        return AuthController.logout()

    # Map routes
    @app.route('/test_map')
    def test_map():
        return MapController.show_map()

    # Context processors
    @app.context_processor
    def inject_active_orders():
        return {'has_active_orders': OrderController.has_active_orders()}

    @app.context_processor
    def utility_processor():
        return dict(datetime=datetime)

    # Admin routes
    @app.route('/admin/products')
    @login_required
    @admin_required
    def admin_products():
        return ProductController.admin_products()

    @app.route('/admin/products/create', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def admin_create_product():
        return ProductController.create()

    @app.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def admin_edit_product(id):
        return ProductController.edit(id)

    @app.route('/admin/products/delete/<int:id>', methods=['POST'])
    @login_required
    @admin_required
    def admin_delete_product(id):
        return ProductController.delete(id) 