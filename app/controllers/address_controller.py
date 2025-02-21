from flask import jsonify, request
from app.auth import get_current_user, login_required
from app.services.address_service import AddressService

class AddressController:
    @staticmethod
    @login_required
    def save_address():
        """Save delivery address for user"""
        user = get_current_user()
        address_data = request.json
        
        if AddressService.save_address(user, address_data):
            return jsonify({'success': True})
        return jsonify({'success': False}) 