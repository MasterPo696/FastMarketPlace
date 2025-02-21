from flask import render_template
from app.auth import login_required

class MapController:
    @staticmethod
    def show_map():
        """Display map page"""
        return render_template('test_map.html')

    @staticmethod
    @login_required
    def show_delivery_map():
        """Display delivery map page"""
        return render_template('delivery_map.html') 