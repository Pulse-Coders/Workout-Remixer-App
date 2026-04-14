from sqlmodel import Session, select
from app.models.workout import Workout

class RemixService:
    def __init__(self, db: Session):
        self.db = db

    def evolve_exercise(self, current_id: int):
        current = self.db.get(Workout, current_id)

        if not current or not current.progression_family: 
            return current

        evolved = self.db.exec(
            select(Workout).where(
                Workout.progression_family == current.progression_family,
                Workout.tier == current.tier + 1
            )
        ).first()

        return evolved if evolved else current 

    def regress_exercise(self, current_id: int):
        current = self.db.get(Workout, current_id)
        
        if not current or not current.progression_family: 
            return current

        easier = self.db.exec(
            select(Workout).where(
                Workout.progression_family == current.progression_family,
                Workout.tier == current.tier - 1
            )
        ).first()

        return easier if easier else current