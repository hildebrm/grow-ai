from beanie import Document
from pydantic import Field, BaseModel
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from ..core.types import PyObjectId

class WorkoutExercise(Document):
    """Individual exercise within a workout with sets/reps configuration"""
    exercise_id: PyObjectId = Field(...)
    sets: int = Field(ge=1)
    reps: int = Field(ge=1) 
    weight: Optional[float] = None  # in kg
    rest_time: Optional[int] = None  # in seconds
    notes: Optional[str] = None
    order: int = Field(ge=1)  # Order of exercise in workout
    
    class Settings:
        collection = "workout_exercises"

class Workout(Document):
    """A workout template containing multiple exercises"""
    
    name: str = Field(...)
    description: Optional[str] = None
    user_id: PyObjectId = Field(...)
    exercises: List[PyObjectId] = []  # References to WorkoutExercise documents
    estimated_duration: Optional[int] = None  # in minutes
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    tags: List[str] = []  # e.g., ["push", "upper_body", "strength"]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Settings:
        collection = "workouts"