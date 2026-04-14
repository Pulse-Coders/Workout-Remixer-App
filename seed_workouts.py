import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session
from app.models.workout import Workout

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URI")
engine = create_engine(DATABASE_URL)

sample_workouts = [
    Workout(
        name="Dumbbell Flyes",
        muscle_group="Chest",
        difficulty="Intermediate",
        equipment="Dumbbells",
        instructions="Lie on bench, arms extended, lower dumbbells out to sides.",
        image_url="/static/img/workouts/chest_fly.jpg"
    ),
    Workout(
        name="Pull-up",
        muscle_group="Back",
        difficulty="Advanced",
        equipment="Bodyweight",
        instructions="Hang from bar, pull chest to bar.",
        image_url="/static/img/workouts/pullup.jpg"
    ),
    Workout(
        name="Squat",
        muscle_group="Legs",
        difficulty="Beginner",
        equipment="Bodyweight",
        instructions="Lower hips back and down, keep chest up.",
        image_url="/static/img/workouts/squat.jpg"
    ),
    Workout(
        name="Shoulder Press",
        muscle_group="Shoulders",
        difficulty="Intermediate",
        equipment="Dumbbells",
        instructions="Press dumbbells overhead from shoulders.",
        image_url="/static/img/workouts/shoulder_press.jpg"
    ),
]

with Session(engine) as session:
    for w in sample_workouts:
        session.add(w)
    session.commit()
    print(f"Added {len(sample_workouts)} workouts.")