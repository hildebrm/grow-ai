from beanie import Document
from pydantic import Field
from typing import List, Optional
from datetime import datetime

class Exercise(Document):
    name: str = Field(...)
    description: Optional[str] = None
    muscle_groups: List[str] = Field(default_factory=list)  # ["chest", "shoulders", "triceps"]
    equipment: Optional[str] = None  # "barbell", "dumbbell", "bodyweight"
    instructions: List[str] = Field(default_factory=list)  # Step by step instructions
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        collection = "exercises"