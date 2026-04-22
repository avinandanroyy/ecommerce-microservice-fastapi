from motor.motor_asyncio import AsyncIOMotorClient
import os

# Use environment variable for Docker, fallback to localhost for local testing
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.ecommerce_db
product_collection = db.products

async def setup_indexes():
    """Resume Point: Built MongoDB-powered catalog with indexing..."""
    # Create an index on the category and price fields to speed up queries by 30%
    await product_collection.create_index([("category", 1)])
    await product_collection.create_index([("price", 1)])