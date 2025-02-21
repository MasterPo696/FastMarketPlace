from app.config import db
from sqlalchemy.ext.hybrid import hybrid_property

class Category(db.Model):
    __bind_key__ = None  # Использует основную БД (products.db)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subcategories = db.relationship('Subcategory', backref='category', lazy=True)

    def __repr__(self):
        return self.name

class Subcategory(db.Model):
    __bind_key__ = None  # Использует основную БД
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    items = db.relationship('Item', backref='subcategory', lazy=True)

    def __repr__(self):
        return f'{self.category.name} - {self.name}'

class Item(db.Model):
    __bind_key__ = None  # Использует основную БД
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Integer, default=0)
    weight = db.Column(db.Float)
    _amount = db.Column('amount', db.Integer, default=0)
    image_path = db.Column(db.String(200))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    isAvailable = db.Column(db.Boolean, default=True)

    @property
    def discounted_price(self):
        if self.discount:
            return round(self.price * (1 - self.discount / 100), 2)
        return self.price

    @hybrid_property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value
        self.isAvailable = value > 0

    def update_amount(self, quantity):
        if self.amount < quantity:
            return False
        self.amount -= quantity
        return True

    def __repr__(self):
        return f'{self.title} (ID: {self.id})' 