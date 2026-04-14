from sqlmodel import Session, SQLModel, select
from app.database import engine 

from app.models.user import User 
from app.models.workout import Workout, Routine, RoutineWorkoutLink

def seed_database():
    print("Building database tables...")
    SQLModel.metadata.create_all(engine)
    
    # Safety check to prevent duplicate seeding
    with Session(engine) as session:
        existing = session.exec(select(Workout)).first()
        if existing:
            print("Database already seeded!")
            return

    # THE RPG SKILL TREES
    expanded_workouts = [
        # --- PUSH-UP SKILL TREE ---
        {"name": "Knee Push-ups", "muscle_group": "Chest", "difficulty": "Beginner", "equipment": "Bodyweight", "instructions": "Standard push-ups but on your knees.", "progression_family": "Push-up", "tier": 1, "xp_reward": 25},
        {"name": "Standard Push-ups", "muscle_group": "Chest", "difficulty": "Intermediate", "equipment": "Bodyweight", "instructions": "Classic push-up.", "progression_family": "Push-up", "tier": 2, "xp_reward": 50},
        {"name": "Decline Push-ups", "muscle_group": "Chest", "difficulty": "Advanced", "equipment": "Bodyweight", "instructions": "Feet elevated on a bench or chair.", "progression_family": "Push-up", "tier": 3, "xp_reward": 100},
        {"name": "Weighted Push-ups", "muscle_group": "Chest", "difficulty": "Advanced", "equipment": "Weight Plate", "instructions": "Push-ups with a weight plate on your back.", "progression_family": "Push-up", "tier": 4, "xp_reward": 200},
        
        # --- SQUAT SKILL TREE ---
        {"name": "Bodyweight Squats", "muscle_group": "Legs", "difficulty": "Beginner", "equipment": "Bodyweight", "instructions": "Basic squat motion.", "progression_family": "Squat", "tier": 1, "xp_reward": 25},
        {"name": "Goblet Squats", "muscle_group": "Legs", "difficulty": "Intermediate", "equipment": "Dumbbells", "instructions": "Squat while holding a dumbbell at chest level.", "progression_family": "Squat", "tier": 2, "xp_reward": 50},
        {"name": "Barbell Squats", "muscle_group": "Legs", "difficulty": "Advanced", "equipment": "Barbell", "instructions": "Rest the barbell on your upper back.", "progression_family": "Squat", "tier": 3, "xp_reward": 100},
        
        # --- PULL SKILL TREE ---
        {"name": "Dumbbell Rows", "muscle_group": "Back", "difficulty": "Beginner", "equipment": "Dumbbells", "instructions": "Support one knee and hand on a bench.", "progression_family": "Pull", "tier": 1, "xp_reward": 25},
        {"name": "Assisted Pull-ups", "muscle_group": "Back", "difficulty": "Intermediate", "equipment": "Bodyweight", "instructions": "Use a band to assist the pull-up.", "progression_family": "Pull", "tier": 2, "xp_reward": 50},
        {"name": "Pull-ups", "muscle_group": "Back", "difficulty": "Advanced", "equipment": "Bodyweight", "instructions": "Hang from a pull-up bar with an overhand grip.", "progression_family": "Pull", "tier": 3, "xp_reward": 100},
        
        # --- CORE SKILL TREE ---
        {"name": "Crunches", "muscle_group": "Core", "difficulty": "Beginner", "equipment": "Bodyweight", "instructions": "Basic abdominal crunch.", "progression_family": "Core", "tier": 1, "xp_reward": 25},
        {"name": "Plank", "muscle_group": "Core", "difficulty": "Intermediate", "equipment": "Bodyweight", "instructions": "Support your body on your forearms and toes.", "progression_family": "Core", "tier": 2, "xp_reward": 50},
        {"name": "Russian Twists", "muscle_group": "Core", "difficulty": "Advanced", "equipment": "Bodyweight", "instructions": "Sit on the floor with your knees bent and twist.", "progression_family": "Core", "tier": 3, "xp_reward": 100}
    ]
    
    print("Injecting RPG workouts...")
    with Session(engine) as session:
        for workout in expanded_workouts:
            new_workout = Workout(**workout)
            session.add(new_workout)
            
        try:
            session.commit()
            print("Database successfully seeded with RPG workouts!")
        except Exception as e:
            session.rollback()
            print(f"CRITICAL ERROR: {e}")
            raise e # Forces the backend to properly report the failure!

if __name__ == "__main__":
    seed_database()