from app.config import db

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
    amount = db.Column(db.Integer, nullable=False)
    isAvailable = db.Column(db.Boolean, default=True)
    
    image_path = db.Column(db.String(200))
    

    def __repr__(self):
        return f'{self.title}' 