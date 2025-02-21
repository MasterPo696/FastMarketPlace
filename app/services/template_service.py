from flask import url_for
from app.models.product_models import Item
from app.auth import get_current_user
import random

class TemplateService:
    @staticmethod
    def shuffle_filter(seq):
        """Custom filter for shuffling sequences"""
        result = list(seq)
        random.shuffle(result)
        return result

    @staticmethod
    def format_price(price):
        """Format price with 2 decimal places"""
        return f"${price:.2f}"

    @staticmethod
    def get_item_image_url(item: Item):
        """Get full URL for item image"""
        if item.image_path:
            return url_for('static', filename=item.image_path)
        return url_for('static', filename='images/default.jpg')

    @staticmethod
    def init_template_globals(app):
        """Initialize template global variables and filters"""
        app.jinja_env.filters['shuffle'] = TemplateService.shuffle_filter
        app.jinja_env.filters['price'] = TemplateService.format_price
        
        app.jinja_env.globals.update(
            get_current_user=get_current_user,
            get_item_image_url=TemplateService.get_item_image_url
        ) 