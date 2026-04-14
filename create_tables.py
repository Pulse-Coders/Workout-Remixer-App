import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URI")
engine = create_engine(DATABASE_URL)

# Import all models so SQLModel knows about them
from app.models.user import User        # Required for foreign key in Routine
from app.models.workout import Workout  # Workout and Routine

# Create tables (order is handled automatically)
SQLModel.metadata.create_all(engine)

print("Tables created successfully!")