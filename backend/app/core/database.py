from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .config import settings
from typing import Optional

mongodb_client: Optional[AsyncIOMotorClient] = None

async def connect_to_mongo():
    """Create database connection"""
    global mongodb_client
    mongodb_client = AsyncIOMotorClient(settings.mongodb_url)
    
    from ..models.user import User
    
    # Ensure database_name is not None
    if settings.database_name is None:
        raise ValueError("settings.database_name cannot be None")
    await init_beanie(
        database=mongodb_client[settings.database_name],
        document_models=[User]
    )

async def close_mongo_connection():
    """Close database connection"""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()

async def get_database():
    """Get database instance"""
    if mongodb_client is None:
        raise RuntimeError("MongoDB client is not initialized")
    if settings.database_name is None:
        raise ValueError("settings.database_name cannot be None")
    return mongodb_client[settings.database_name]