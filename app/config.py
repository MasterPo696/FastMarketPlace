from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Получаем путь к корневой директории проекта
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, 
    template_folder=os.path.join(basedir, 'templates'),  # путь к шаблонам
    static_folder=os.path.join(basedir, 'static')        # путь к статическим файлам
)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///shop.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static/images')

db = SQLAlchemy(app=app)