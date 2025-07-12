from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Optional
from bson import ObjectId
from .core.database import connect_to_mongo, close_mongo_connection, get_database
from .core.config import settings
from .models.exercise import Exercise
from .schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    print("Connected to MongoDB")
    yield
    # Shutdown
    await close_mongo_connection()
    print("Disconnected from MongoDB")

app = FastAPI(
    title=settings.app_name or "Grow AI",
    version=settings.app_version or "0.1.0",
    description="Fitness tracking and workout planning API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
# app.include_router(exercise.router, prefix="/api/v1")

# Exercise endpoints for testing
@app.post("/api/v1/exercises", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(exercise_data: ExerciseCreate):
    """Create a new exercise"""
    try:
        exercise = Exercise(**exercise_data.dict())
        await exercise.insert()
        return ExerciseResponse(
            id=str(exercise.id),
            **exercise.dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating exercise: {str(e)}"
        )

@app.get("/api/v1/exercises", response_model=List[ExerciseResponse])
async def get_exercises(
    skip: int = 0,
    limit: int = 100,
    muscle_group: Optional[str] = None,
    difficulty: Optional[str] = None,
    equipment: Optional[str] = None
):
    """Get all exercises with optional filtering"""
    try:
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching exercises: {str(e)}"
        )

@app.get("/api/v1/exercises/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(exercise_id: str):
    """Get a specific exercise by ID"""
    try:
        if not ObjectId.is_valid(exercise_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid exercise ID format"
            )
        
        exercise = await Exercise.get(ObjectId(exercise_id))
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exercise not found"
            )
        return ExerciseResponse(
            id=str(exercise.id),
            **exercise.dict()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching exercise: {str(e)}"
        )

@app.put("/api/v1/exercises/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(exercise_id: str, exercise_data: ExerciseUpdate):
    """Update an existing exercise"""
    try:
        if not ObjectId.is_valid(exercise_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid exercise ID format"
            )
        
        exercise = await Exercise.get(ObjectId(exercise_id))
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exercise not found"
            )
        
        # Update only provided fields
        update_data = exercise_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(exercise, field, value)
        
        await exercise.save()
        return ExerciseResponse(
            id=str(exercise.id),
            **exercise.dict()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating exercise: {str(e)}"
        )

@app.delete("/api/v1/exercises/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(exercise_id: str):
    """Delete an exercise"""
    try:
        if not ObjectId.is_valid(exercise_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid exercise ID format"
            )
        
        exercise = await Exercise.get(ObjectId(exercise_id))
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exercise not found"
            )
        
        await exercise.delete()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting exercise: {str(e)}"
        )

@app.get("/")
async def root():
    return {"message": f"{settings.app_name} is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

@app.get("/test-db")
async def test_db():
    try:
        db = await get_database()
        return {"status": "connected", "collections": await db.list_collection_names()}
    except Exception as e:
        return {"status": "error", "message": str(e)}