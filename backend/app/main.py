from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .core.database import connect_to_mongo, close_mongo_connection, get_database
from .core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    print("Connected to MongoDB")
    yield
    # Shutdown
    await close_mongo_connection()
    print("Disconnected from MongoDB")

app = FastAPI(
    title=settings.app_name or "Grow AI",
    version=settings.app_version or "0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": f"{settings.app_name} is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

@app.get("/test-db")
async def test_db():
    try:
        db = await get_database()
        return {"status": "connected", "collections": await db.list_collection_names()}
    except Exception as e:
        return {"status": "error", "message": str(e)}