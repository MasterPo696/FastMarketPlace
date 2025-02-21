from flask import Flask
from toml import load
from app.config import app, db
from app.services.template_service import TemplateService
from app.services.item_service import ItemService
from app.services.cart_service import CartService
from app.auth import get_current_user
import random

def init_app():
    # Load config
    config = load('secrets/config.toml')
    app.config.update({
        'PUBLIC': config['public'],
        'SECRET': config['secret']
    })

    # Add custom filter to Jinja environment
    def shuffle_filter(seq):
        result = list(seq)
        random.shuffle(result)
        return result

    app.jinja_env.filters['shuffle'] = shuffle_filter

    # Initialize template globals
    TemplateService.init_template_globals(app)
    app.jinja_env.globals.update(
        get_item=ItemService.get_item,
        get_cart_total=CartService.get_cart_total,
        get_current_user=get_current_user
    )

    return app 