from typing import List, Optional
from bson import ObjectId
from beanie.odm.operators.find.comparison import In

from ..models.exercise import Exercise
from ..schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse

class ExerciseService:
    """Service layer for exercise operations"""
    
    async def create_exercise(self, exercise_data: ExerciseCreate) -> ExerciseResponse:
        """Create a new exercise"""
        exercise = Exercise(**exercise_data.dict())
        await exercise.insert()
        return ExerciseResponse(
            id=str(exercise.id),
            **exercise.dict()
        )
    
    async def get_exercises(
        self, 
        skip: int = 0, 
        limit: int = 100,
        muscle_group: Optional[str] = None,
        difficulty: Optional[str] = None,
        equipment: Optional[str] = None
    ) -> List[ExerciseResponse]:
        """Get exercises with optional filtering"""
        query = {}
        
        if muscle_group:
            query["muscle_groups"] = {"$in": [muscle_group]}
        if difficulty:
            query["difficulty"] = difficulty
        if equipment:
            query["equipment"] = equipment
        
        exercises = await Exercise.find(query).skip(skip).limit(limit).to_list()
        return [
            ExerciseResponse(
                id=str(exercise.id),
                **exercise.dict()
            ) for exercise in exercises
        ]
    
    async def get_exercise_by_id(self, exercise_id: str) -> Optional[ExerciseResponse]:
        """Get a specific exercise by ID"""
        exercise = await Exercise.get(ObjectId(exercise_id))
        if exercise:
            return ExerciseResponse(
                id=str(exercise.id),
                **exercise.dict()
            )
        return None
    
    async def update_exercise(
        self, 
        exercise_id: str, 
        exercise_data: ExerciseUpdate
    ) -> Optional[ExerciseResponse]:
        """Update an existing exercise"""
        exercise = await Exercise.get(ObjectId(exercise_id))
        if not exercise:
            return None
        
        # Update only provided fields
        update_data = exercise_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(exercise, field, value)
        
        await exercise.save()
        return ExerciseResponse(
            id=str(exercise.id),
            **exercise.dict()
        )
    
    async def delete_exercise(self, exercise_id: str) -> bool:
        """Delete an exercise"""
        exercise = await Exercise.get(ObjectId(exercise_id))
        if exercise:
            await exercise.delete()
            return True
        return False