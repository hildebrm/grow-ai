from beanie import Document
from pydantic import Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class SessionExercise(Document):
    """Actual performance of an exercise during a workout session"""
    exercise_id: ObjectId = Field(...)
    workout_exercise_id: ObjectId = Field(...)  # Reference to planned exercise
    sets_completed: int = Field(ge=0)
    actual_sets: List[dict] = []  # [{"reps": 12, "weight": 50.0, "rpe": 8}]
    notes: Optional[str] = None
    skipped: bool = False
    completed_at: Optional[datetime] = None
    
    class Settings:
        collection = "session_exercises"

class WorkoutSession(Document):
    """A completed workout session"""
    workout_id: ObjectId = Field(...)
    user_id: ObjectId = Field(...)
    split_id: Optional[ObjectId] = None  # If part of a split
    session_name: Optional[str] = None
    exercises: List[ObjectId] = []  # References to SessionExercise documents
    
    # Session timing
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    duration: Optional[int] = None  # in minutes
    
    # Session metrics
    total_volume: Optional[float] = None  # Total weight lifted (kg)
    total_reps: Optional[int] = None
    total_sets: Optional[int] = None
    
    # Session status
    status: str = "in_progress"  # in_progress, completed, abandoned
    completion_percentage: Optional[float] = None
    
    # Notes and ratings
    notes: Optional[str] = None
    difficulty_rating: Optional[int] = Field(None, ge=1, le=10)
    energy_level: Optional[int] = Field(None, ge=1, le=10)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        collection = "sessions"