from beanie import Document
from pydantic import Field
from typing import List, Optional, Dict
from datetime import datetime
from bson import ObjectId
from ..core.types import PyObjectId

class SplitDay(Document):
    """A day within a workout split"""
    day_name: str = Field(...)  # e.g., "Push Day", "Pull Day", "Legs"
    workout_id: PyObjectId = Field(...)
    day_number: int = Field(ge=1)  # 1-7 for weekly splits
    rest_day: bool = False
    
    class Settings:
        collection = "split_days"

class WorkoutSplit(Document):
    """A workout split containing multiple days/workouts"""
    name: str = Field(...)
    description: Optional[str] = None
    user_id: PyObjectId = Field(...)
    days: List[PyObjectId] = []  # References to SplitDay documents
    split_type: str = Field(...)  # e.g., "push_pull_legs", "upper_lower", "full_body"
    weeks_duration: Optional[int] = None  # How many weeks this split runs
    is_active: bool = False  # Whether this is the user's current split
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Settings:
        collection = "splits"