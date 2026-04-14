from fastapi import Request, HTTPException
from pydantic import BaseModel
from sqlmodel import select

from app.dependencies.session import SessionDep 
from . import api_router

from app.services.user_service import UserService
from app.repositories.user import UserRepository
from app.schemas import UserResponse

from app.models.workout import Workout
from app.services.remix_service import RemixService
from app.utilities.seed import seed_database

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# ==========================================
# USER MANAGEMENT ENDPOINTS
# ==========================================

@api_router.get("/users", response_model=list[UserResponse])
async def list_users(request: Request, db: SessionDep):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service.get_all_users()


# ==========================================
# WORKOUT & REMIX ENDPOINTS
# ==========================================

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


# ==========================================
# DATABASE UTILITIES
# ==========================================

@api_router.get("/trigger-seed")
async def trigger_seed():
    try:
        seed_database()
        return {"message": "Database successfully seeded!"}
    except Exception as e:
        return {"error": str(e)}


# ==========================================
# AI CHATBOT INTEGRATION
# ==========================================

class ChatMessage(BaseModel):
    message: str

@api_router.post("/chat")
async def ai_chat_endpoint(chat_msg: ChatMessage):
    try:
        llm = ChatOpenAI(
            base_url="https://ai-gen.sundaebytestt.com/v1",
            api_key="sk-59addf63a8bd464c92242421db666aa1",
            model="meta/llama-3.2-3b-instruct"
        )
        
        messages = [
            SystemMessage(content="You are FitBot, a helpful and concise fitness assistant."),
            HumanMessage(content=chat_msg.message)
        ]
        
        response = await llm.ainvoke(messages)
        return {"reply": str(response.content)}
        
    except Exception as e:
        return {"reply": f"AI ERROR: {str(e)}"}