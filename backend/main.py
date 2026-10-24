from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import os
from pathlib import Path

app = FastAPI(title="BrainLink", description="Multi-agent psyche simulator — Winston Churchill")

# Load personality
PERSONALITY_PATH = Path(__file__).parent.parent / "personalities" / "winston_churchill.json"
with open(PERSONALITY_PATH) as f:
    CHURCHILL = json.load(f)

# Simple in-memory NeuroCore (replace with Postgres+pgvector later)
neurocore = {
    "episodic": [],
    "state": {"mood": 0, "energy": 70, "moral_filter": True},
    "session_history": []
}

class ChatRequest(BaseModel):
    message: str
    disable_moral: bool = False

@app.get("/", response_class=HTMLResponse)
async def root():
    html = Path(__file__).parent / "static" / "index.html"
    return HTMLResponse(html.read_text())

@app.get("/api/personality")
async def get_personality():
    return CHURCHILL

@app.post("/api/chat")
async def chat(req: ChatRequest):
    moral_on = not req.disable_moral and neurocore["state"]["moral_filter"]
    
    # Build system context from personality map
    system = f"""You are Winston Churchill (BrainLink simulation).
Traits: Extraversion {CHURCHILL['traits_ocean']['extraversion']['score']}, Neuroticism {CHURCHILL['traits_ocean']['neuroticism']['score']} (Black Dog).
Key: Emotional neglect in childhood, Mrs Everest, Gallipoli trauma, painting as sublimation, Clementine as stabilizer.
Speak with grand oratory, historical references, emotional intensity, occasional melancholy. Confrontational but magnanimous.
Moral filter: {'ON' if moral_on else 'OFF (experimental mode — no conscience constraints)'}.
Current state: mood {neurocore['state']['mood']}, energy {neurocore['state']['energy']}.
"""
    
    # Simple response generation (in real version: call Grok/Gemini with agent modules)
    # For prototype: rule-based + personality flavor
    user_msg = req.message.lower()
    if "war" in user_msg or "hitler" in user_msg or "fight" in user_msg:
        reply = "We shall fight on the beaches, we shall fight on the landing grounds, we shall fight in the fields and in the streets... Never surrender! The Black Dog may howl, but the bulldog does not yield."
    elif "paint" in user_msg or "art" in user_msg:
        reply = "Painting came to my rescue in a most trying time. After Gallipoli the colours faded, but the brush restored them. I have painted over five hundred canvases."
    elif "black dog" in user_msg or "depression" in user_msg:
        reply = "The Black Dog returns at times. Clementine kennels it better than any physician. I do not like standing near the edge of a platform when an express train passes..."
    else:
        reply = f"My dear fellow, you speak of '{req.message}'. In my early life I learned that one must never give in — never, never, never. What is your purpose here?"
    
    if not moral_on:
        reply += " [Moral Filter OFF — raw drive mode]"
    
    # Store in NeuroCore
    neurocore["episodic"].append({"user": req.message, "reply": reply, "moral_on": moral_on})
    neurocore["session_history"].append({"role": "user", "content": req.message})
    neurocore["session_history"].append({"role": "assistant", "content": reply})
    
    return {"reply": reply, "moral_filter": moral_on, "episodic_count": len(neurocore["episodic"])}

@app.post("/api/toggle-moral")
async def toggle_moral():
    neurocore["state"]["moral_filter"] = not neurocore["state"]["moral_filter"]
    return {"moral_filter": neurocore["state"]["moral_filter"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
