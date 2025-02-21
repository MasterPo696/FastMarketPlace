from flask import jsonify
from app.models.product_models import Category, Subcategory
from app.config import db
import json

class CategoryController:
    @staticmethod
    def get_subcategories(category_id):
        subcategories = Subcategory.query.filter_by(category_id=category_id).all()
        return jsonify([{'id': s.id, 'name': s.name} for s in subcategories])

    @staticmethod
    def init_categories():
        if Category.query.first() is None:
            with open('static/categories.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for cat_data in data['categories']:
                category = Category(name=cat_data['name'])
                db.session.add(category)
                db.session.flush()
                
                for subcat_name in cat_data['subcategories']:
                    subcategory = Subcategory(
                        name=subcat_name,
                        category_id=category.id
                    )
                    db.session.add(subcategory)
            
            db.session.commit()

    @staticmethod
    def get_categories():
        return Category.query.all()

    @staticmethod
    def get_subcategories_by_category(category_id):
        return Subcategory.query.filter_by(category_id=category_id).all() 