from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client: AsyncIOMotorClient = None
db = None


async def connect_db():
    global client, db
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]
    await db.users.create_index("email", unique=True)
    await db.resumes.create_index("user_id")
    await db.analyses.create_index("resume_id")


async def close_db():
    global client
    if client:
        client.close()


def get_db():
    return db
