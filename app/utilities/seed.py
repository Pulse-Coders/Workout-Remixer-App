from sqlmodel import Session, SQLModel
from app.database import engine 

from app.models.user import User 

from app.models.workout import Workout, Routine, RoutineWorkoutLink

def seed_database():
    print("Building database tables...")
    SQLModel.metadata.create_all(engine)
    
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
            name="Dumbbell Flyes", 
            muscle_group="Chest", 
            equipment="Dumbbells", 
            difficulty="Intermediate", 
            instructions="Slight bend in elbows, lower weights out to sides."
        ),
 
        Workout(
            name="Bodyweight Squat", 
            muscle_group="Legs", 
            equipment="Bodyweight", 
            difficulty="Beginner", 
            instructions="Keep chest up, push hips back and down."
        ),
        Workout(
            name="Dumbbell Lunge", 
            muscle_group="Legs", 
            equipment="Dumbbells", 
            difficulty="Intermediate", 
            instructions="Step forward, lower hips until both knees are bent at 90 degrees."
        ),

        Workout(
            name="Pull-up", 
            muscle_group="Back", 
            equipment="Bodyweight", 
            difficulty="Advanced", 
            instructions="Grip bar overhead, pull body up until chin clears the bar."
        ),
        Workout(
            name="Dumbbell Row", 
            muscle_group="Back", 
            equipment="Dumbbells", 
            difficulty="Beginner", 
            instructions="Pull dumbbell to hip, keeping back straight."
        )
    ]
    
    print("Injecting default workouts...")
    with Session(engine) as session:
        for workout in initial_workouts:
            session.add(workout)
            
        try:
            session.commit()
            print("Database successfully seeded with default workouts!")
        except Exception as e:
            session.rollback()
            print(f"Something went wrong: {e}")

if __name__ == "__main__":
    seed_database()