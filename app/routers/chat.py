from fastapi import Request
from fastapi.responses import JSONResponse
from . import api_router
import re

@api_router.post("/chat")
async def chat(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    if not messages:
        return JSONResponse({"reply": "Please ask something!"})
    
    user_msg = messages[-1]["content"].lower().strip()
    
    # ----- Helper to detect intent -----
    def has_words(words):
        return any(word in user_msg for word in words)
    
    # ----- Chest -----
    if has_words(["chest", "pec", "bench", "push up", "pushup"]):
        reply = """💪 **Chest exercises:** 
- Dumbbell Flyes (3x10-12)
- Bench Press (3x8-10)
- Push-ups (3x failure)
- Incline Press (upper chest)

**Easy start:** Do 3 sets of knee push-ups, then progress to regular push-ups."""
    
    # ----- Back -----
    elif has_words(["back", "pull up", "pullup", "row", "lat"]):
        reply = """🏋️ **Back exercises:** 
- Pull-ups (assisted or lat pulldown)
- Bent-over Rows (3x10)
- Deadlifts (3x5)
- Seated Cable Rows

**Easy start:** Use resistance bands for rows, or do inverted rows under a table."""
    
    # ----- Legs -----
    elif has_words(["leg", "squat", "lunge", "glute", "quad", "hamstring"]):
        reply = """🦵 **Leg exercises:** 
- Bodyweight Squats (3x15)
- Lunges (3x10 per leg)
- Glute Bridges (3x15)
- Calf Raises (3x20)

**Easy start:** Just bodyweight squats and lunges – no equipment needed."""
    
    # ----- Shoulders -----
    elif has_words(["shoulder", "deltoid", "overhead press", "lateral raise"]):
        reply = """💪 **Shoulder exercises:** 
- Overhead Press (dumbbells or barbell)
- Lateral Raises (light weight)
- Front Raises
- Face Pulls (for rear delts)

**Easy start:** Use water bottles as weights for lateral raises."""
    
    # ----- Arms -----
    elif has_words(["arm", "bicep", "tricep", "curl", "dip"]):
        reply = """💪 **Arm exercises:** 
- Bicep Curls (3x12)
- Tricep Dips (3x10)
- Hammer Curls
- Overhead Tricep Extension

**Easy start:** Use resistance bands or light household items."""
    
    # ----- Core / Abs -----
    elif has_words(["core", "ab", "abs", "plank", "crunch"]):
        reply = """🔥 **Core exercises:** 
- Plank (hold 20-60s)
- Bicycle Crunches (3x15)
- Leg Raises (3x12)
- Russian Twists

**Easy start:** Start with lying heel taps and short planks."""
    
    # ----- Cardio -----
    elif has_words(["cardio", "run", "jog", "walk", "bike", "swim", "heart"]):
        reply = """❤️ **Cardio options:** 
- Brisk walking (30 min)
- Jogging / Running
- Cycling
- Jump rope
- Swimming

**Easy start:** Walk for 10 minutes, then gradually increase duration and speed."""
    
    # ----- Nutrition / Diet -----
    elif has_words(["eat", "food", "diet", "protein", "calorie", "meal"]):
        reply = """🥗 **Nutrition tips:** 
- Eat protein with every meal (chicken, fish, eggs, beans)
- Include vegetables and whole grains
- Stay hydrated (2-3 liters water daily)
- Avoid sugary drinks

**For weight loss:** Slight calorie deficit, more protein, less processed food."""
    
    # ----- Beginner / Easy workout -----
    elif has_words(["easy", "beginner", "new", "start", "simple"]):
        reply = """🌟 **Beginner full body workout (no equipment):**
1. Bodyweight squats – 3x12
2. Push-ups (or knee push-ups) – 3x8
3. Lunges – 3x10 per leg
4. Plank – 3x20 seconds
5. Glute bridges – 3x15

Do this 3 times per week. Rest 60s between sets."""
    
    # ----- Motivation / General -----
    elif has_words(["motivation", "how to start", "give up", "consistent"]):
        reply = """🔥 **Staying motivated:**
- Set small, achievable goals (e.g., workout 2x this week)
- Track your progress in a journal
- Find a workout buddy
- Reward yourself after completing a week

Remember: Consistency beats intensity. Start small and build habit."""
    
    # ----- Greetings -----
    elif has_words(["hello", "hi", "hey", "greetings"]):
        reply = "Hello! I'm FitBot. Ask me about chest, back, legs, shoulders, arms, core, cardio, nutrition, or beginner workouts. What would you like to know?"
    
    # ----- Default / Anything else -----
    else:
        reply = f"""Thanks for asking: "{messages[-1]['content']}"

I can help with:
- Specific muscle groups (chest, back, legs, shoulders, arms, core)
- Cardio and fat loss
- Beginner/easy workouts
- Nutrition tips
- Motivation

Just tell me what you're interested in!"""
    
    return JSONResponse({"reply": reply})