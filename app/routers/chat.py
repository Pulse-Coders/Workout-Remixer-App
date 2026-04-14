from fastapi import Request
from fastapi.responses import JSONResponse
from . import api_router
import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are FitBot, an AI assistant for the Workout Remixer app.
You help users with:
- Suggesting workouts and routines based on their goals, equipment, and fitness level
- Answering fitness and exercise questions
- Navigating the Workout Remixer app (finding routines, using filters, remixing workouts)
- General fitness and health advice

Keep responses concise, friendly, and motivating.
If asked about something unrelated to fitness or the app, politely redirect the conversation."""

@api_router.post("/chat")
async def chat(request: Request):
    body = await request.json()
    messages = body.get("messages", [])

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages
    )

    return JSONResponse({"reply": response.content[0].text})