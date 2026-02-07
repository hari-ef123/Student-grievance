import asyncio
import models
import database
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def list_users():
    # Re-use database connection logic
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    await database.init_db([models.User])
    
    users = await models.User.find_all().to_list()
    print("-" * 50)
    print(f"{'NAME':<20} | {'EMAIL':<30} | {'ROLE':<10}")
    print("-" * 50)
    for user in users:
        print(f"{user.name:<20} | {user.email:<30} | {user.role:<10}")
    print("-" * 50)

if __name__ == "__main__":
    asyncio.run(list_users())
