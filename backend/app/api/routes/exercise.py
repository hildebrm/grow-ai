from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from bson import ObjectId
from beanie.odm.operators.find.comparison import In

from ...models.exercise import Exercise
from ...schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse
from ...services.exercise import ExerciseService

router = APIRouter(prefix="/exercises", tags=["exercises"])

# Dependency injection for service
def get_exercise_service() -> ExerciseService:
    return ExerciseService()

@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(
    exercise_data: ExerciseCreate,
    service: ExerciseService = Depends(get_exercise_service)
):
    """Create a new exercise"""
    try:
        return await service.create_exercise(exercise_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating exercise: {str(e)}"
        )

@router.get("/", response_model=List[ExerciseResponse])
async def get_all_exercises(
    skip: int = 0,
    limit: int = 100,
    muscle_group: Optional[str] = None,
    difficulty: Optional[str] = None,
    equipment: Optional[str] = None,
    service: ExerciseService = Depends(get_exercise_service)
):
    """Get all exercises with optional filtering"""
    try:
        return await service.get_exercises(
            skip=skip, 
            limit=limit, 
            muscle_group=muscle_group,
            difficulty=difficulty,
            equipment=equipment
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching exercises: {str(e)}"
        )

@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(
    exercise_id: str,
    service: ExerciseService = Depends(get_exercise_service)
):
    """Get a specific exercise by ID"""
    try:
        if not ObjectId.is_valid(exercise_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid exercise ID format"
            )
        
        exercise = await service.get_exercise_by_id(exercise_id)
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exercise not found"
            )
        return exercise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching exercise: {str(e)}"
        )

@router.put("/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: str,
    exercise_data: ExerciseUpdate,
    service: ExerciseService = Depends(get_exercise_service)
):
    """Update an existing exercise"""
    try:
        if not ObjectId.is_valid(exercise_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid exercise ID format"
            )
        
        updated_exercise = await service.update_exercise(exercise_id, exercise_data)
        if not updated_exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exercise not found"
            )
        return updated_exercise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating exercise: {str(e)}"
        )

@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(
    exercise_id: str,
    service: ExerciseService = Depends(get_exercise_service)
):
    """Delete an exercise"""
    try:
        if not ObjectId.is_valid(exercise_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid exercise ID format"
            )
        
        deleted = await service.delete_exercise(exercise_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exercise not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting exercise: {str(e)}"
        )