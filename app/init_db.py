from app.config import app, db
from app.models.product_models import Category, Subcategory, Item
from app.models.user_models import User, Receipt
from app.models.order_models import Order
import os
import json

def init_databases():
    """Initialize databases if they don't exist"""
    with app.app_context():
        # Создаем все таблицы во всех базах данных
        db.create_all()
        
        # Создаем таблицы в каждой базе данных отдельно
        for bind_key in ['users', 'orders']:
            engine = db.get_engine(app, bind=bind_key)
            tables = [table for table in db.metadata.tables.values()
                     if getattr(table, 'info', {}).get('bind_key') == bind_key]
            db.metadata.create_all(bind=engine, tables=tables)
        
        # Инициализируем категории из JSON
        init_categories_from_json()

def init_categories_from_json():
    """Initialize categories from JSON file"""
    try:
        if Category.query.first() is None:
            json_path = os.path.join(app.static_folder, 'categories.json')
            
            with open(json_path, 'r', encoding='utf-8') as f:
                categories_data = json.load(f)
            
            for category_data in categories_data['categories']:
                category = Category(name=category_data['name'])
                db.session.add(category)
                db.session.flush()  # Получаем ID категории
                
                for subcat_name in category_data['subcategories']:
                    subcategory = Subcategory(
                        name=subcat_name,
                        category_id=category.id
                    )
                    db.session.add(subcategory)
                
            db.session.commit()
            print("Categories initialized from JSON successfully")
    except Exception as e:
        print(f"Error initializing categories from JSON: {str(e)}")
        db.session.rollback()

if __name__ == '__main__':
    init_databases()

def drop_databases():
    with app.app_context():
        # Удаляем все таблицы из всех баз данных
        db.session.remove()  # Закрываем все сессии
        db.drop_all()
        
        # Удаляем таблицы из каждой базы данных отдельно
        for bind_key in ['users', 'orders']:
            engine = db.get_engine(app, bind=bind_key)
            tables = [table for table in db.metadata.tables.values()
                     if getattr(table, 'info', {}).get('bind_key') == bind_key]
            db.metadata.drop_all(bind=engine, tables=tables)

def reset_user_and_order_databases():
    """Reset only user and order databases"""
    if os.path.exists('users.db'):
        os.remove('users.db')
    if os.path.exists('orders.db'):
        os.remove('orders.db')
    
    with app.app_context():
        # Создаем таблицы в каждой базе данных отдельно
        for bind_key in ['users', 'orders']:
            engine = db.get_engine(app, bind=bind_key)
            tables = [table for table in db.metadata.tables.values()
                     if getattr(table, 'info', {}).get('bind_key') == bind_key]
            db.metadata.create_all(bind=engine, tables=tables)

def init_categories():
    """Initialize categories if they don't exist"""
    try:
        # Проверяем, есть ли уже категории
        if Category.query.first() is None:
            # Создаем базовые категории
            categories = [
                ("Фрукты", ["Цитрусовые", "Тропические", "Сезонные"]),
                ("Овощи", ["Корнеплоды", "Листовые", "Томаты и перцы"]),
                ("Напитки", ["Соки", "Вода", "Газировка"]),
            ]
            
            for cat_name, subcats in categories:
                category = Category(name=cat_name)
                db.session.add(category)
                db.session.flush()
                print(f"Created category: {cat_name}")
                
                for subcat_name in subcats:
                    subcategory = Subcategory(name=subcat_name, category_id=category.id)
                    db.session.add(subcategory)
                    print(f"Created subcategory: {subcat_name}")
            
            db.session.commit()
            print("Categories initialized successfully")
            # Выведем существующие категории
            categories = Category.query.all()
            for cat in categories:
                print(f"Category: {cat.name}")
                for subcat in cat.subcategories:
                    print(f"  - Subcategory: {subcat.name}")
                    
        else:
            print("Categories already exist")
            
    except Exception as e:
        print(f"Error initializing categories: {str(e)}")
        db.session.rollback() 