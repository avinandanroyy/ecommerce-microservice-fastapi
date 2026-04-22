from fastapi import FastAPI, HTTPException
from . import schemas, transactions
import uuid

app = FastAPI(title="Order Service", description="Transactional Order Processing")

# Mock DB for orders
orders_db = []

@app.post("/orders", response_model=schemas.Order)
async def create_order(order_req: schemas.OrderCreate):
    # 1. Start Transaction: Attempt to deduct stock from Product Service
    await transactions.validate_and_deduct_stock(order_req.product_id, order_req.quantity)
    
    try:
        # 2. Simulate Payment Processing or Database Commit
        # If this crashes, the `except` block catches it and rolls back
        
        # Fake calculating price (in reality, fetch from product service)
        calculated_price = 99.99 * order_req.quantity 
        
        new_order = schemas.Order(
            id=str(uuid.uuid4()),
            user_id=order_req.user_id,
            product_id=order_req.product_id,
            quantity=order_req.quantity,
            status="COMPLETED",
            total_price=calculated_price
        )
        orders_db.append(new_order)
        return new_order
        
    except Exception as e:
        # 3. Rollback Mechanism triggered if order creation fails!
        await transactions.rollback_stock(order_req.product_id, order_req.quantity)
        raise HTTPException(status_code=500, detail="Order processing failed, transaction rolled back.")