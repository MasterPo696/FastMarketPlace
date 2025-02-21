from typing import List, Optional
from src.core.interfaces.repositories import ProductRepository
from src.core.models.product import Product
from .models import ProductModel

class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, id: int) -> Optional[Product]:
        product_model = self.session.query(ProductModel).get(id)
        return self._to_domain(product_model) if product_model else None

    def list_by_category(self, category_id: int) -> List[Product]:
        products = self.session.query(ProductModel)\
            .join(ProductModel.subcategory)\
            .filter(Subcategory.category_id == category_id)\
            .all()
        return [self._to_domain(p) for p in products]

    def _to_domain(self, model: ProductModel) -> Product:
        return Product(
            id=model.id,
            title=model.title,
            price=model.price,
            description=model.description,
            weight=model.weight,
            amount=model.amount,
            image_path=model.image_path,
            subcategory_id=model.subcategory_id,
            is_available=model.is_available,
            discount=model.discount
        ) 