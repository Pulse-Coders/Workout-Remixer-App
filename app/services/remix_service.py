from sqlmodel import Session, select
from app.models.workout import Workout
import random

class RemixService:
    def __init__(self, session: Session):
        self.session = session

    def get_remixed_workout(self, current_workout_id: int):
        current_workout = self.session.get(Workout, current_workout_id)

        if not current_workout:
            return None

        statement = select(Workout).where(
            Workout.muscle_group == current_workout.muscle_group,
            Workout.id != current_workout_id
        )
        alternatives = self.session.exec(statement).all()

        if not alternatives:
            return current_workout
            
        return random.choice(alternatives)