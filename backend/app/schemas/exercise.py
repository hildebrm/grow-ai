from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Request Schemas
class ExerciseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    muscle_groups: List[str] = []
    equipment: Optional[str] = None
    instructions: List[str] = []
    difficulty: str = "beginner"

class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    muscle_groups: Optional[List[str]] = None
    equipment: Optional[str] = None
    instructions: Optional[List[str]] = None
    difficulty: Optional[str] = None

# Response Schemas
class ExerciseResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    muscle_groups: List[str] = []
    equipment: Optional[str] = None
    instructions: List[str] = []
    difficulty: str
    created_at: datetime

    class Config:
        from_attributes = True