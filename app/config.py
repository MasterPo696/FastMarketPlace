from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from datetime import timedelta

# Получаем путь к корневой директории проекта
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, 
    template_folder=os.path.join(basedir, 'templates'),  # путь к шаблонам
    static_folder=os.path.join(basedir, 'static')        # путь к статическим файлам
)

# Конфигурация
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
    SQLALCHEMY_DATABASE_URI='sqlite:///products.db',
    SQLALCHEMY_BINDS={
        'users': 'sqlite:///users.db',
        'orders': 'sqlite:///orders.db'
    },
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    PERMANENT_SESSION_LIFETIME=timedelta(days=31),
    UPLOAD_FOLDER=os.path.join(basedir, 'static/images')
)

# Инициализация расширений
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Импортируем модели после создания db
from app.models import *