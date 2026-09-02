from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone


class Review(BaseModel):
    rating: float
    reviewer_name: str
    review_text: str


class Product(BaseModel):
    id: int = Field(alias="_id")   # MongoDB calls it "_id", we want to use "id" in Python code
    name: str
    category: str
    price: float
    description: str
    is_organic: bool = False
    reviews: list[Review] = []
    avg_rating: float = 0.0

    class Config:
        populate_by_name = True   # lets us create a Product using either "id" or "_id"

class CartItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int = 1


class Cart(BaseModel):
    id: str = Field(alias="_id", default="main_cart")
    items: list[CartItem] = []

    class Config:
        populate_by_name = True

class Order(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    items: list[CartItem]
    total: float
    ordered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True