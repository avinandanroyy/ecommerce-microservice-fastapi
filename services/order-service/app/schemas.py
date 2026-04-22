from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: str
    product_id: str
    quantity: int

class Order(OrderCreate):
    id: str
    status: str
    total_price: float