from app.models.product_models import Category, Item, Subcategory
from app.models.user_models import User
from app.config import db, app
from werkzeug.security import generate_password_hash
import os

class InitController:
    @staticmethod
    def init_admin():
        """Initialize admin user"""
        try:
            # Check if admin exists
            admin = User.query.filter_by(email='admin@example.com').first()
            if not admin:
                admin = User(
                    email='admin@example.com',
                    password_hash=generate_password_hash('admin'),
                    is_admin=True,
                    is_verified=True
                )
                db.session.add(admin)
                db.session.commit()
                print("Admin user created successfully")
            else:
                print("Admin user already exists")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating admin user: {str(e)}")
            print(f"Error creating admin user: {str(e)}")

    @staticmethod
    def add_test_product():
        """Add test product"""
        try:
            # Check if test product exists
            test_product = Item.query.filter_by(title='Banana').first()
            if not test_product:
                # Create categories if they don't exist
                categories = Category.query.all()
                if not categories:
                    fruit_category = Category(name='Fruits')
                    db.session.add(fruit_category)
                    db.session.commit()
                    
                    fruit_subcategory = Subcategory(
                        name='Fresh Fruits',
                        category_id=fruit_category.id
                    )
                    db.session.add(fruit_subcategory)
                    db.session.commit()
                else:
                    fruit_subcategory = Subcategory.query.first()

                # Create test product
                test_product = Item(
                    title='Banana',
                    description='Fresh yellow banana',
                    price=1.99,
                    weight=150,
                    amount=100,
                    image_path='images/banana.jpg',
                    subcategory_id=fruit_subcategory.id,
                    is_active=True
                )
                db.session.add(test_product)
                db.session.commit()
                print("Test product created successfully")
            else:
                print("Test product already exists")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error adding test product: {str(e)}")
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
                image_dir = os.path.join(app.static_folder, 'images')
                if not os.path.exists(image_dir):
                    os.makedirs(image_dir)
                
                # Путь к изображению
                image_path = 'images/banana.jpg'
                full_image_path = os.path.join(app.static_folder, image_path)
                
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