from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class RoutineWorkoutLink(SQLModel, table=True):
    routine_id: Optional[int] = Field(default=None, foreign_key="routine.id", primary_key=True)
    workout_id: Optional[int] = Field(default=None, foreign_key="workout.id", primary_key=True)

class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    muscle_group: str
    equipment: str   
    difficulty: str    
    instructions: str
    image_url: Optional[str] = None
    
    routines: List["Routine"] = Relationship(back_populates="workouts", link_model=RoutineWorkoutLink)

class Routine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    
    user_id: int = Field(default=None, foreign_key="user.id") 
    
    workouts: List[Workout] = Relationship(back_populates="routines", link_model=RoutineWorkoutLink)