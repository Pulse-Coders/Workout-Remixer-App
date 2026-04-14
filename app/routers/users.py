from fastapi import Request, HTTPException, status
from pydantic import BaseModel
from sqlmodel import select, SQLModel # Added SQLModel for reset logic
from typing import List

from app.dependencies.session import SessionDep 
from app.database import engine # Added engine for reset logic
from . import api_router

from app.services.user_service import UserService
from app.repositories.user import UserRepository
from app.schemas import UserResponse

from app.models.workout import Workout
from app.services.remix_service import RemixService
from app.utilities.seed import seed_database

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# --- SCHEMAS FOR CONVERSATION HISTORY ---
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# --- USER MANAGEMENT ---
@api_router.get("/users", response_model=list[UserResponse])
async def list_users(request: Request, db: SessionDep):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service.get_all_users()

# --- WORKOUTS & RPG LOGIC ---
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

# EMERGENCY RESET: Use this to fix the "UndefinedColumn" PostgreSQL error
@api_router.get("/debug-db-reset")
async def debug_db_reset():
    try:
        # This deletes OLD tables and creates NEW ones with all RPG columns
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        return {"message": "Database wiped and rebuilt with new RPG columns! Your data is now clean."}
    except Exception as e:
        return {"error": str(e)}

# --- CONSOLIDATED AI CHATBOT ---
@api_router.post("/chat")
async def ai_chat_endpoint(chat_data: ChatRequest):
    try:
        user_input = chat_data.messages[-1].content

        llm = ChatOpenAI(
            # Added /v1 to match standard LangChain requirements
            base_url="https://ai-gen.sundaebytestt.com/v1", 
            api_key="sk-59addf63a8bd464c92242421db666aa1",
            model="meta/llama-3.2-3b-instruct",
            max_tokens=150,
            timeout=15.0 
        )
 
        messages = [SystemMessage(content="You are FitBot, a helpful fitness assistant. Keep answers under 3 sentences.")]
        
        for m in chat_data.messages:
            if m.role == "user":
                messages.append(HumanMessage(content=m.content))
        
        response = await llm.ainvoke(messages)
        return {"reply": str(response.content)}
        
    except Exception as e:
        print(f"AI Connection Error: {e}")
        user_text = chat_data.messages[-1].content.lower()
        
        def has_words(words):
            return any(word in user_text for word in words)
        
        if has_words(["chest", "push up", "pushup"]):
            return {"reply": "For your chest, focus on Standard Push-ups and Evolve them into Decline Push-ups as you gain strength!"}
        elif has_words(["back", "pull up", "row"]):
            return {"reply": "Try Bent-over Rows or Pull-ups for a stronger back. You can Simplify pull-ups by using a band!"}
        elif has_words(["leg", "squat", "lunge"]):
            return {"reply": "Bodyweight squats and lunges are a great foundation. Level them up once they feel too easy."}
        elif has_words(["level", "xp", "rank"]):
            return {"reply": "You earn XP by building and saving routines! Higher tier exercises give you more XP toward your next level."}
        elif has_words(["hello", "hi", "hey"]):
            return {"reply": "Hello! I'm FitBot. I'm currently in offline mode, but I can still help with basic workout advice. What's on your mind?"}
        else:
            return {"reply": "I'm having trouble connecting to the AI, but keep crushing those routines! Try asking about specific muscle groups like 'chest' or 'legs'."}