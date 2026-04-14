import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, select
from app.models.workout import Workout

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URI")
engine = create_engine(DATABASE_URL)

with Session(engine) as session:
    workouts = session.exec(select(Workout)).all()
    for w in workouts:
        print(f"{w.name}: {w.image_url}")