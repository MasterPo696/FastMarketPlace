from typing import List, Optional
from src.core.models.product import Product
from src.core.interfaces.repositories import ProductRepository

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def get_product(self, id: int) -> Optional[Product]:
        return self.product_repository.get_by_id(id)

    def list_products_by_category(self, category_id: int) -> List[Product]:
        return self.product_repository.list_by_category(category_id)

    def create_product(self, product_data: dict) -> Product:
        # Бизнес-логика создания продукта
        pass

    def update_stock(self, product_id: int, quantity: int) -> bool:
        product = self.get_product(product_id)
        if not product or product.amount < quantity:
            return False
        
        product.amount -= quantity
        product.is_available = product.amount > 0
        self.product_repository.update(product)
        return True 