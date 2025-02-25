from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_object('app.config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'migrations'))

# Import routes after app initialization
from app.controllers import cart_controller, product_controller, auth_controller, order_controller 