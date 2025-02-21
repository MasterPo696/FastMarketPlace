from app.models.product_models import Item

class ItemService:
    @staticmethod
    def get_item(item_id: int) -> Item:
        """Get item by ID"""
        return Item.query.get(int(item_id)) 