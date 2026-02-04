
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_mongo():
    try:
        client = AsyncIOMotorClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
        await client.server_info()
        print("SUCCESS: MongoDB is running and accessible.")
    except Exception as e:
        print(f"ERROR: Could not connect to MongoDB. {e}")

if __name__ == "__main__":
    asyncio.run(check_mongo())
