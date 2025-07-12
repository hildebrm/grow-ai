from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Request Schemas
class WorkoutExerciseCreate(BaseModel):
    exercise_id: str = Field(...)
    sets: int = Field(ge=1)
    reps: int = Field(ge=1)
    weight: Optional[float] = None
    rest_time: Optional[int] = None
    notes: Optional[str] = None
    order: int = Field(ge=1)

class WorkoutCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    exercises: List[WorkoutExerciseCreate] = []
    estimated_duration: Optional[int] = None
    difficulty: str = "beginner"
    tags: List[str] = []

class WorkoutUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    exercises: Optional[List[WorkoutExerciseCreate]] = None
    estimated_duration: Optional[int] = None
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = None

class WorkoutExerciseResponse(BaseModel):
    id: str
    exercise_id: str
    sets: int
    reps: int
    weight: Optional[float] = None
    rest_time: Optional[int] = None
    notes: Optional[str] = None
    order: int

class WorkoutResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    user_id: str
    exercises: List[WorkoutExerciseResponse] = []
    estimated_duration: Optional[int] = None
    difficulty: str
    tags: List[str] = []
    created_at: datetime
    updated_at: Optional[datetime] = None