from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Request Schemas
class SplitDayCreate(BaseModel):
    day_name: str = Field(..., min_length=1, max_length=50)
    workout_id: str = Field(...)
    day_number: int = Field(ge=1, le=7)
    rest_day: bool = False

class WorkoutSplitCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    days: List[SplitDayCreate] = []
    split_type: str = Field(...)
    weeks_duration: Optional[int] = None

class WorkoutSplitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    split_type: Optional[str] = None
    weeks_duration: Optional[int] = None
    is_active: Optional[bool] = None

# Response Schemas
class SplitDayResponse(BaseModel):
    id: str
    day_name: str
    workout_id: str
    day_number: int
    rest_day: bool

class WorkoutSplitResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    user_id: str
    days: List[SplitDayResponse] = []
    split_type: str
    weeks_duration: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None