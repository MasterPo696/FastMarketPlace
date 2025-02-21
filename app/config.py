from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import secrets

# Получаем путь к корневой директории проекта
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, 
    template_folder=os.path.join(basedir, 'templates'),  # путь к шаблонам
    static_folder=os.path.join(basedir, 'static')        # путь к статическим файлам
)

# Генерируем случайный секретный ключ
app.secret_key = secrets.token_hex(16)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///shop.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static/images')

db = SQLAlchemy(app)

# Импортируем модели после создания db
from app.models import *