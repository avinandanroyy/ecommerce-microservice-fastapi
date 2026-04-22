from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    stock_quantity: int

class Product(ProductCreate):
    id: str = Field(alias="_id")