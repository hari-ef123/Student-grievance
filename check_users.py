import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from backend import models, database

async def list_users():
    client = AsyncIOMotorClient(database.MONGODB_URL)
    await init_beanie(database=client[database.DATABASE_NAME], document_models=[models.User])
    
    users = await models.User.all().to_list()
    print(f"Total Users: {len(users)}")
    for user in users:
        print(f"- {user.email} ({user.role})")

if __name__ == "__main__":
    asyncio.run(list_users())
