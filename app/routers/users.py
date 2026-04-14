from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Form, status
from sqlmodel import select

from app.dependencies import SessionDep
from app.dependencies.session import SessionDep
from . import api_router
from app.services.user_service import UserService
from app.services.remix_service import RemixService
from app.repositories.user import UserRepository
from app.utilities.flash import flash
from app.schemas import UserResponse
from app.models.workout import Workout


@api_router.get("/users", response_model=list[UserResponse])
async def list_users(request: Request, db: SessionDep):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service.get_all_users()

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