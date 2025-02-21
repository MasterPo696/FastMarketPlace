from flask_migrate import Migrate
from app.config import app, db

migrate = Migrate(app, db)