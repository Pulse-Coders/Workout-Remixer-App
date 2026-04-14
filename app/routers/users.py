from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, status, Form
from app.dependencies import SessionDep
from . import api_router
from app.services.user_service import UserService
from app.repositories.user import UserRepository
from app.utilities.flash import flash
from app.schemas import UserResponse
from fastapi import HTTPException
from app.dependencies.session import SessionDep 
from app.services.remix_service import RemixService


# API endpoint for listing users
@api_router.get("/users", response_model=list[UserResponse])
async def list_users(request: Request, db: SessionDep):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service.get_all_users()

@api_router.get("/remix/{workout_id}")
async def remix_exercise(workout_id: int, db: SessionDep):
    remix_svc = RemixService(db)
    new_workout = remix_svc.get_remixed_workout(workout_id)

    if not new_workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    return new_workout

from sqlmodel import select
from app.models.workout import Workout

@api_router.get("/workouts")
async def get_all_workouts(db: SessionDep):
    workouts = db.exec(select(Workout)).all()
    return workouts

from fastapi import HTTPException
from sqlmodel import select
from app.dependencies.session import SessionDep 
from app.models.workout import Workout
from app.services.remix_service import RemixService

@api_router.get("/workouts")
async def get_all_workouts(db: SessionDep):
    workouts = db.exec(select(Workout)).all()
    return workouts

@api_router.get("/remix/{workout_id}")
async def remix_exercise(workout_id: int, db: SessionDep):
    remix_svc = RemixService(db)
    new_workout = remix_svc.get_remixed_workout(workout_id)
    
    if not new_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
        
    return new_workout

from app.utilities.seed import seed_database

@api_router.get("/trigger-seed")
async def trigger_seed():
    try:
        seed_database()
        return {"message": "Database successfully seeded!"}
    except Exception as e:
        return {"error": str(e)}