import asyncio
import motor.motor_asyncio
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

async def populate_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    database_name = os.getenv("DATABASE_NAME")
    if database_name is None:
        raise ValueError("DATABASE_NAME environment variable is not set")
    db = client[database_name]

    try:
        print("Populating exercises collection...")
        exercises_data = [
            {
                "name": "Push-ups",
                "description": "Classic bodyweight exercise for chest, shoulders, and triceps",
                "muscle_groups": ["chest", "shoulders", "triceps"],
                "equipment": "bodyweight",
                "instructions": [
                    "Start in a plank position with hands shoulder-width apart",
                    "Lower your body until chest nearly touches the floor",
                    "Push back up to starting position",
                    "Keep your body straight throughout the movement"
                ],
                "difficulty": "beginner",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Bench Press",
                "description": "Compound movement for chest, shoulders, and triceps using barbell",
                "muscle_groups": ["chest", "shoulders", "triceps"],
                "equipment": "barbell",
                "instructions": [
                    "Lie on bench with feet flat on floor",
                    "Grip barbell with hands slightly wider than shoulder-width",
                    "Lower bar to chest with control",
                    "Press bar back up to starting position"
                ],
                "difficulty": "intermediate",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Squats",
                "description": "Fundamental lower body exercise targeting quads, glutes, and hamstrings",
                "muscle_groups": ["quadriceps", "glutes", "hamstrings"],
                "equipment": "bodyweight",
                "instructions": [
                    "Stand with feet shoulder-width apart",
                    "Lower body as if sitting back into a chair",
                    "Keep chest up and knees over toes",
                    "Return to standing position"
                ],
                "difficulty": "beginner",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Deadlift",
                "description": "Compound movement targeting posterior chain",
                "muscle_groups": ["hamstrings", "glutes", "erector_spinae", "traps"],
                "equipment": "barbell",
                "instructions": [
                    "Stand with feet hip-width apart, bar over mid-foot",
                    "Bend at hips and knees to grip bar",
                    "Keep chest up and back straight",
                    "Drive through heels to lift bar"
                ],
                "difficulty": "advanced",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Pull-ups",
                "description": "Upper body pulling exercise for back and biceps",
                "muscle_groups": ["latissimus_dorsi", "biceps", "rhomboids"],
                "equipment": "pull_up_bar",
                "instructions": [
                    "Hang from bar with palms facing away",
                    "Pull body up until chin clears bar",
                    "Lower with control to starting position",
                    "Avoid swinging or kipping"
                ],
                "difficulty": "intermediate",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Plank",
                "description": "Core stability exercise",
                "muscle_groups": ["core", "shoulders"],
                "equipment": "bodyweight",
                "instructions": [
                    "Start in push-up position on forearms",
                    "Keep body straight from head to heels",
                    "Hold position while breathing normally",
                    "Don't let hips sag or pike up"
                ],
                "difficulty": "beginner",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Dumbbell Rows",
                "description": "Unilateral back exercise using dumbbells",
                "muscle_groups": ["latissimus_dorsi", "rhomboids", "biceps"],
                "equipment": "dumbbell",
                "instructions": [
                    "Place one knee and hand on bench",
                    "Hold dumbbell in opposite hand",
                    "Pull dumbbell to side of torso",
                    "Lower with control"
                ],
                "difficulty": "beginner",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Shoulder Press",
                "description": "Overhead pressing movement for shoulders",
                "muscle_groups": ["shoulders", "triceps"],
                "equipment": "dumbbell",
                "instructions": [
                    "Stand with dumbbells at shoulder height",
                    "Press weights overhead until arms are extended",
                    "Lower with control to starting position",
                    "Keep core engaged throughout"
                ],
                "difficulty": "intermediate",
                "created_at": datetime.utcnow()
            }
        ]
        
        # Clear existing exercises and insert new ones
        await db.exercises.delete_many({})
        result = await db.exercises.insert_many(exercises_data)
        print(f"✅ Inserted {len(result.inserted_ids)} exercises")
        
        # 3. Get exercise IDs for workouts
        exercises = await db.exercises.find({}).to_list(length=None)
        exercise_lookup = {ex["name"]: ex["_id"] for ex in exercises}
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(populate_db())