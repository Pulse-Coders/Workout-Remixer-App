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

# --- SCHEMAS ---
class ChatMessage(BaseModel):
    message: str

# --- USER MANAGEMENT ---
@api_router.get("/users", response_model=list[UserResponse])
async def list_users(request: Request, db: SessionDep):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service.get_all_users()

# --- WORKOUTS & RPG LOGIC ---
# 👇 THIS IS THE ROUTE THAT WENT MISSING!
@api_router.get("/workouts")
async def get_all_workouts(db: SessionDep):
    workouts = db.exec(select(Workout)).all()
    return workouts

@api_router.get("/evolve/{workout_id}")
async def evolve_exercise_route(workout_id: int, db: SessionDep):
    remix_svc = RemixService(db)
    return remix_svc.evolve_exercise(workout_id)

@api_router.get("/regress/{workout_id}")
async def regress_exercise_route(workout_id: int, db: SessionDep):
    remix_svc = RemixService(db)
    return remix_svc.regress_exercise(workout_id)

# --- DATABASE UTILITIES ---
@api_router.get("/trigger-seed")
async def trigger_seed():
    try:
        seed_database()
        return {"message": "Database successfully seeded!"}
    except Exception as e:
        return {"error": str(e)}

# --- AI CHATBOT (LANGCHAIN) ---
@api_router.post("/chat")
async def ai_chat_endpoint(chat_msg: ChatMessage):
    try:
        # Try to connect to your class's custom LLM server
        llm = ChatOpenAI(
            base_url="https://ai-gen.sundaebytestt.com/v1",
            api_key="sk-59addf63a8bd464c92242421db666aa1",
            model="meta/llama-3.2-3b-instruct",
            max_tokens=150,
            timeout=5.0 # Stop waiting after 5 seconds so the app doesn't freeze
        )
        
        messages = [
            SystemMessage(content="You are FitBot, a helpful, energetic, and concise fitness assistant. Keep answers under 3 sentences."),
            HumanMessage(content=chat_msg.message)
        ]
        
        response = await llm.ainvoke(messages)
        return {"reply": str(response.content)}
        
    except Exception as e:
        print(f"⚠️ AI Server Error: {e}")
        # THE FALLBACK: If the server is dead, use this local mock bot!
        user_text = chat_msg.message.lower()
        if "chest" in user_text or "push" in user_text:
            return {"reply": "For a great chest workout, try combining Standard Push-ups with Dumbbell Bench Presses! Aim for 3 sets of 10."}
        elif "leg" in user_text or "squat" in user_text:
            return {"reply": "Never skip leg day! Barbell Squats and Lunges are the absolute best foundation for lower body strength."}
        elif "level" in user_text or "xp" in user_text:
            return {"reply": "You earn XP by building and saving routines! The harder the exercise Tier, the more XP you get. Keep grinding!"}
        else:
            return {"reply": "I'm currently operating in offline mode! I can still recommend workouts if you ask me about specific muscles like 'chest', 'legs', or 'back'."}