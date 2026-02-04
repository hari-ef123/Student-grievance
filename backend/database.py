from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

# MongoDB connection string
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "student_grievance"

async def init_db(models: list):
    client = AsyncIOMotorClient(MONGODB_URL)
    await init_beanie(database=client[DATABASE_NAME], document_models=models)
