from app.config import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class User(db.Model):
    __bind_key__ = 'users'  # Использует users.db
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    auth_token = db.Column(db.String(100), unique=True)
    token_expiry = db.Column(db.DateTime)
    verification_code = db.Column(db.String(10))
    code_expiry = db.Column(db.DateTime)
    address = db.Column(db.JSON, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def generate_auth_token(self):
        self.auth_token = secrets.token_urlsafe(32)
        self.token_expiry = datetime.now() + timedelta(days=30)

class Receipt(db.Model):
    __bind_key__ = 'users'  # Использует users.db
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100), nullable=False)
    card_number = db.Column(db.String(19), nullable=False)
    cardholder_name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    items = db.Column(db.JSON, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref='orders') 