from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserProfile(BaseModel):
    age: Optional[int] = None
    weight: Optional[float] = None  # in kg
    height: Optional[int] = None    # in cm
    fitness_level: Optional[str] = "beginner"  # beginner, intermediate, advanced

class User(Document):
    email: EmailStr = Field(...)
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile: Optional[UserProfile] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Settings:
        collection = "users"