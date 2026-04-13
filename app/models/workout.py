from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

# Link table for the Many-to-Many relationship
class RoutineWorkoutLink(SQLModel, table=True):
    routine_id: Optional[int] = Field(default=None, foreign_key="routine.id", primary_key=True)
    workout_id: Optional[int] = Field(default=None, foreign_key="workout.id", primary_key=True)

class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    muscle_group: str  # e.g., "Chest", "Legs", "Back"
    equipment: str     # e.g., "Dumbbells", "Bodyweight", "Barbell"
    difficulty: str    # e.g., "Beginner", "Intermediate", "Advanced"
    instructions: str
    
    # Links back to the routines this workout is part of
    routines: List["Routine"] = Relationship(back_populates="workouts", link_model=RoutineWorkoutLink)

class Routine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    
    # Links to the User table (assuming the user model is named 'user')
    user_id: int = Field(default=None, foreign_key="user.id") 
    
    # Links to the workouts inside this routine
    workouts: List[Workout] = Relationship(back_populates="routines", link_model=RoutineWorkoutLink)