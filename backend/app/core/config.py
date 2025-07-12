from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    mongodb_url: str | None = os.getenv("MONGODB_URL")
    database_name: str | None = os.getenv("DATABASE_NAME")

    app_name: str | None = os.getenv("APP_NAME")
    app_version: str | None = os.getenv("APP_VERSION")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()