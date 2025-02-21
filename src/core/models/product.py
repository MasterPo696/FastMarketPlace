from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class Product:
    id: Optional[int]
    title: str
    price: Decimal
    description: str
    weight: float
    amount: int
    image_path: Optional[str]
    subcategory_id: int
    is_available: bool = True
    discount: int = 0

    @property
    def discounted_price(self) -> Decimal:
        if self.discount:
            return round(self.price * (1 - self.discount / 100), 2)
        return self.price 