from app.config import db
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subcategories = db.relationship('Subcategory', backref='category', lazy=True)

    def __repr__(self):
        return self.name

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    items = db.relationship('Item', backref='subcategory', lazy=True)

    def __repr__(self):
        return f'{self.category.name} - {self.name}'

class Item(db.Model):
    # Основные данные
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Цена и скидка
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    
    # Связь с категорией
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)
    
    @property
    def discounted_price(self):
        if self.discount:
            return round(self.price * (1 - self.discount / 100), 2)
        return self.price
    

    # Количество и доступность
    _amount = db.Column('amount', db.Integer, nullable=False)
    isAvailable = db.Column(db.Boolean, default=True)
    
    image_path = db.Column(db.String(200))
    

    def __repr__(self):
        return f'{self.title}'

    def update_amount(self, quantity):
        """
        Updates the item amount after purchase.
        Returns False if there's insufficient stock.
        """
        if self.amount < quantity:
            return False
        self.amount -= quantity
        self.isAvailable = self.amount > 0  # Automatically update isAvailable
        return True

    @hybrid_property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value
        self.isAvailable = value > 0

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100), nullable=False)
    card_number = db.Column(db.String(19), nullable=False)
    cardholder_name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    items = db.Column(db.JSON, nullable=False)
    
    # Исправляем связь с пользователем
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f'Receipt #{self.order_id}'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # For session management
    auth_token = db.Column(db.String(100), unique=True)
    token_expiry = db.Column(db.DateTime)
    
    # Verification
    verification_code = db.Column(db.String(10))
    code_expiry = db.Column(db.DateTime)
    
    # Relationship with orders
    orders = db.relationship('Receipt', backref='user', lazy=True)
    
    # New field for address
    address = db.Column(db.JSON, nullable=True)  # Will store coordinates and address details
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def generate_auth_token(self):
        self.auth_token = secrets.token_urlsafe(32)
        self.token_expiry = datetime.now() + timedelta(days=30)
        
    def is_token_valid(self):
        return (self.auth_token and self.token_expiry 
                and datetime.now() < self.token_expiry) 