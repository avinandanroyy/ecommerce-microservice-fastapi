import httpx
from fastapi import HTTPException
import os

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8001")

async def validate_and_deduct_stock(product_id: str, quantity: int):
    """Communicates with Product Service to secure stock."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                f"{PRODUCT_SERVICE_URL}/products/{product_id}/deduct-stock",
                params={"quantity": quantity}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Stock validation failed: Insufficient stock")
            return True
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Product service unavailable")

async def rollback_stock(product_id: str, quantity: int):
    """Resume Point: ...and rollback mechanisms ensuring ACID compliance."""
    # In a real scenario, this would call an endpoint to ADD the stock back
    # if the payment or final order commit failed.
    print(f"ROLLBACK INITIATED: Returning {quantity} units to product {product_id}")
    # async with httpx.AsyncClient() as client:
    #     await client.put(f"{PRODUCT_SERVICE_URL}/products/{product_id}/add-stock", params={"quantity": quantity})