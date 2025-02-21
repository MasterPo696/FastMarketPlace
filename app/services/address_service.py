from app.models.user_models import User
from app.config import db
from typing import Dict, Any

class AddressService:
    @staticmethod
    def save_address(user: User, address_data: Dict[str, Any]) -> bool:
        try:
            user.address = {
                'address': address_data['address'],
                'building': address_data['building'],
                'floor': address_data['floor'],
                'apartment': address_data['apartment'],
                'coordinates': address_data['coordinates']
            }
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error saving address: {str(e)}")
            return False 