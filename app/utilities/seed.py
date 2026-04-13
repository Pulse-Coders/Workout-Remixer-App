
from sqlmodel import Session
from app.dependencies.session import engine # Ensure this path matches our engine location
from app.models.workout import Workout

def seed_database():
    initial_workouts = [
        Workout(
            name="Standard Push-up", 
            muscle_group="Chest", 
            equipment="Bodyweight", 
            difficulty="Beginner", 
            instructions="Keep body straight, lower until chest touches floor."
        ),
        Workout(
            name="Barbell Bench Press", 
            muscle_group="Chest", 
            equipment="Barbell", 
            difficulty="Intermediate", 
            instructions="Lower bar to mid-chest, press up powerfully."
        ),
        Workout(
            name="Dumbbell Row", 
            muscle_group="Back", 
            equipment="Dumbbells", 
            difficulty="Beginner", 
            instructions="Pull dumbbell to hip, keeping back straight."
        ),
        Workout(
            name="Bodyweight Squat", 
            muscle_group="Legs", 
            equipment="Bodyweight", 
            difficulty="Beginner", 
            instructions="Keep chest up, push hips back and down."
        )
    ]
    
    with Session(engine) as session:
        for workout in initial_workouts:
            session.add(workout)
        session.commit()
        print("✅ Database successfully seeded with default workouts!")

if __name__ == "__main__":
    seed_database()
