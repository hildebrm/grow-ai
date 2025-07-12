from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Request Schemas
class SessionExerciseCreate(BaseModel):
    exercise_id: str = Field(...)
    workout_exercise_id: str = Field(...)
    sets_completed: int = Field(ge=0)
    actual_sets: List[dict] = []  # [{"reps": 12, "weight": 50.0, "rpe": 8}]
    notes: Optional[str] = None
    skipped: bool = False

class WorkoutSessionCreate(BaseModel):
    workout_id: str = Field(...)
    split_id: Optional[str] = None
    session_name: Optional[str] = None
    exercises: List[SessionExerciseCreate] = []

class WorkoutSessionUpdate(BaseModel):
    status: Optional[str] = None
    exercises: Optional[List[SessionExerciseCreate]] = None
    notes: Optional[str] = None
    difficulty_rating: Optional[int] = Field(None, ge=1, le=10)
    energy_level: Optional[int] = Field(None, ge=1, le=10)

# Response Schemas
class SessionExerciseResponse(BaseModel):
    id: str
    exercise_id: str
    workout_exercise_id: str
    sets_completed: int
    actual_sets: List[dict] = []
    notes: Optional[str] = None
    skipped: bool
    completed_at: Optional[datetime] = None

class WorkoutSessionResponse(BaseModel):
    id: str
    workout_id: str
    user_id: str
    split_id: Optional[str] = None
    session_name: Optional[str] = None
    exercises: List[SessionExerciseResponse] = []
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration: Optional[int] = None
    total_volume: Optional[float] = None
    total_reps: Optional[int] = None
    total_sets: Optional[int] = None
    status: str
    completion_percentage: Optional[float] = None
    notes: Optional[str] = None
    difficulty_rating: Optional[int] = None
    energy_level: Optional[int] = None
    created_at: datetime