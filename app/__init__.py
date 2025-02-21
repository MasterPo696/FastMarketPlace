# Удаляем или комментируем эти строки
# from app.controllers.init_controller import InitController
# InitController.check_and_fill_database() 

from flask import Flask
import os
from app.config import db, login_manager

def create_app():
    # Создаем экземпляр приложения Flask
    app = Flask(__name__)

    # Конфигурация приложения
    app.config['SECRET_KEY'] = 'your-secret-key'  # Замените на свой секретный ключ
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализируем расширения
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page'
    login_manager.login_message_category = 'info'

    # Создаем директории если их нет
    os.makedirs('static/product_images', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)

    # Импортируем и регистрируем маршруты
    with app.app_context():
        from app import routes
    
    return app 