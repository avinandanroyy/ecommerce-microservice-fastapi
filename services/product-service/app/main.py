from fastapi import FastAPI, HTTPException, status
from typing import List
from bson import ObjectId
from . import schemas, database

app = FastAPI(title="Product Service", description="MongoDB Catalog & Aggregation")

@app.on_event("startup")
async def startup_event():
    await database.setup_indexes()

@app.post("/products", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: schemas.ProductCreate):
    product_dict = product.dict()
    result = await database.product_collection.insert_one(product_dict)
    product_dict["_id"] = str(result.inserted_id)
    return product_dict

@app.get("/products/stats")
async def get_product_stats():
    pipeline = [
        {"$group": {
            "_id": "$category",
            "average_price": {"$avg": "$price"},
            "total_stock": {"$sum": "$stock_quantity"}
        }},
        {"$sort": {"total_stock": -1}}
    ]
    stats = await database.product_collection.aggregate(pipeline).to_list(length=100)
    return {"data": stats}

@app.put("/products/{product_id}/deduct-stock")
async def deduct_stock(product_id: str, quantity: int):
    result = await database.product_collection.update_one(
        {"_id": ObjectId(product_id), "stock_quantity": {"$gte": quantity}},
        {"$inc": {"stock_quantity": -quantity}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Insufficient stock or product not found")
    return {"message": "Stock deducted successfully"}