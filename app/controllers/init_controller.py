from app.models.product_models import Category, Item, Subcategory
from app.models.user_models import User
from app.config import db
from werkzeug.security import generate_password_hash
import os
from app.llm import GigaChatAPI
from flask import current_app

class InitController:
    @staticmethod
    def init_admin():
        """Initialize admin user"""
        try:
            # Check if admin exists
            admin = User.query.filter_by(email='admin@admin').first()
            if not admin:
                admin = User(
                    email='admin@admin',
                    password=generate_password_hash('admin'),
                    is_admin=True
                )
                db.session.add(admin)
                db.session.commit()
                print("Admin user created successfully")
            else:
                print("Admin user already exists")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating admin user: {str(e)}")
            print(f"Error creating admin user: {str(e)}")

    @staticmethod
    def add_test_product():
        """Add test product"""
        try:
            # Check if test product exists
            test_product = Item.query.filter_by(title='Banana').first()
            if not test_product:
                # Проверяем существование категорий
                fruit_category = Category.query.filter_by(name='Фрукты').first()
                if not fruit_category:
                    # Если категорий нет, создаем их
                    from app.init_db import init_categories
                    init_categories()
                    fruit_category = Category.query.filter_by(name='Фрукты').first()
                
                # Получаем подкатегорию "Тропические"
                tropical_subcategory = Subcategory.query.filter_by(
                    name='Тропические', 
                    category_id=fruit_category.id
                ).first()

                if not tropical_subcategory:
                    print("Error: Required subcategory not found")
                    return

                # Create test product
                test_product = Item(
                    title='Banana',
                    description='Fresh yellow banana',
                    price=1.99,
                    weight=150,
                    amount=100,
                    image_path='images/banana.jpg',
                    subcategory_id=tropical_subcategory.id,
                    is_active=True,
                    isAvailable=True
                )
                db.session.add(test_product)
                db.session.commit()
                print(f"Test product created successfully: {test_product.title} (ID: {test_product.id})")
            else:
                print(f"Test product already exists: {test_product.title} (ID: {test_product.id})")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error adding test product: {str(e)}")
            print(f"Error adding test product: {str(e)}")

    @staticmethod
    def add_test_product_old():
        """Add test product if it doesn't exist"""
        try:
            # Проверяем существование товара
            if not Item.query.filter_by(title="Banana").first():
                # Находим подкатегорию
                subcategory = Subcategory.query.filter_by(name="Тропические").first()
                if not subcategory:
                    print("Error: Subcategory 'Тропические' not found")
                    return
                    
                # Проверяем/создаем директорию для изображений
                image_dir = os.path.join(current_app.static_folder, 'images')
                if not os.path.exists(image_dir):
                    os.makedirs(image_dir)
                
                # Путь к изображению
                image_path = 'images/banana.jpg'
                full_image_path = os.path.join(current_app.static_folder, image_path)
                
                # Создаем тестовый товар
                item = Item(
                    title="Banana",
                    description="Fresh bananas from Ecuador",
                    price=10.0,
                    discount=0,
                    weight=100.0,
                    amount=10,
                    subcategory_id=subcategory.id,
                    image_path=image_path,
                    is_active=True,
                    isAvailable=True
                )
                
                try:
                    db.session.add(item)
                    db.session.commit()
                    print(f"Test product added successfully: {item.title}")
                    
                    # Проверяем наличие изображения
                    if not os.path.exists(full_image_path):
                        print(f"Warning: Image file not found at {full_image_path}")
                
                except Exception as e:
                    print(f"Error adding test product: {str(e)}")
                    db.session.rollback()
            else:
                print("Test product already exists")
            
        except Exception as e:
            print(f"Error in add_test_product: {str(e)}")

    @staticmethod
    def check_and_fill_database():
        """Check if database is empty and fill it with initial items if needed"""
        try:
            # Проверяем количество товаров в базе
            items_count = Item.query.count()
            
            if items_count == 0:
                print("Database is empty. Creating initial items...")
                
                # Создаем экземпляр GigaChatAPI
                giga = GigaChatAPI()
                
                # Получаем начальные товары
                initial_items = giga.create_initial_items()
                
                # Добавляем товары в базу данных
                for item_data in initial_items:
                    try:
                        # Находим подкатегорию
                        subcategory = Subcategory.query.filter_by(
                            name=item_data['subcategory']
                        ).first()
                        
                        if not subcategory:
                            print(f"Subcategory {item_data['subcategory']} not found")
                            continue
                        
                        # Создаем новый товар
                        item = Item(
                            title=item_data['name'],
                            description=item_data['description'],
                            price=float(item_data['price']),
                            weight=float(item_data['weight']),
                            discount=int(item_data['discount']),
                            subcategory_id=subcategory.id,
                            image_path=item_data['image_path'],
                            amount=10,  # Дефолтное количество
                            is_active=True,
                            isAvailable=True
                        )
                        
                        db.session.add(item)
                        print(f"Added item: {item.title}")
                        
                    except Exception as e:
                        print(f"Error adding item {item_data['name']}: {str(e)}")
                        continue
                
                # Сохраняем все изменения
                try:
                    db.session.commit()
                    print("Initial items added successfully")
                except Exception as e:
                    db.session.rollback()
                    print(f"Error committing changes: {str(e)}")
            
            else:
                print(f"Database already contains {items_count} items")
                
        except Exception as e:
            print(f"Error in check_and_fill_database: {str(e)}") 