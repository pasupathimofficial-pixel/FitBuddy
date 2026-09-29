import os, json
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

try:
    from google import genai
except ImportError:
    genai = None

BASE = Path(__file__).resolve().parent.parent
load_dotenv(BASE / ".env")

app = FastAPI(title="FitBuddy AI", version="2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class PlanRequest(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    age: int = Field(ge=13, le=100)
    activity: str = "Beginner"
    goal: str = "General fitness"
    days_per_week: int = Field(ge=3, le=7)

class FeedbackRequest(BaseModel):
    feedback: str = Field(min_length=2, max_length=500)

def fallback(d, feedback=None):
    workouts = [
        ("Full-body mobility + light strength","25–35 min"),
        ("Brisk walk + mobility","25–40 min"),
        ("Lower-body bodyweight basics","25–35 min"),
        ("Rest / gentle stretching","10–20 min"),
        ("Upper-body + core basics","25–35 min"),
        ("Light cardio of your choice","20–35 min"),
        ("Recovery walk + stretching","15–25 min"),
    ]
    days=[]
    for i,(w,t) in enumerate(workouts):
        if i >= d.days_per_week: w,t="Rest / gentle mobility","10–20 min"
        days.append({"day":f"Day {i+1}","workout":w,"duration":t,
                     "intensity":"easy to moderate",
                     "notes":"Warm up first, use comfortable form, and stop if you feel pain or unwell."})
    return {"summary":f"A simple {d.days_per_week}-day plan focused on {d.goal.lower()}.",
            "days":days,
            "recovery":"Stay hydrated, eat regular balanced meals, sleep well and allow recovery.",
            "safety":"General wellness information only; not medical advice."}

def make_plan(d, feedback: Optional[str]=None):
    key=os.getenv("GEMINI_API_KEY")
    if not key or genai is None: return fallback(d, feedback)
    try:
        client=genai.Client(api_key=key)
        prompt=f"""Create a safe beginner-friendly 7-day wellness activity plan.
Name:{d.name}; Age:{d.age}; Experience:{d.activity}; Goal:{d.goal}; Active days:{d.days_per_week}; Feedback:{feedback or "none"}.
Return ONLY JSON with summary, days (exactly 7 objects containing day,workout,duration,intensity,notes), recovery,safety.
Do not prescribe medication, supplements, extreme dieting, dangerous exercises, or medical treatment."""
        r=client.models.generate_content(model=os.getenv("GEMINI_MODEL","gemini-2.5-flash"),contents=prompt)
        text=(r.text or "").replace("```json","").replace("```","").strip()
        out=json.loads(text)
        if len(out.get("days",[]))!=7: raise ValueError()
        return out
    except Exception:
        return fallback(d, feedback)

@app.get("/api/health")
def health(): return {"status":"ok"}

@app.post("/api/plan")
def plan(d: PlanRequest): return make_plan(d)

@app.post("/api/plan/feedback")
def feedback(d: PlanRequest, f: FeedbackRequest): return make_plan(d, f.feedback)

app.mount("/", StaticFiles(directory=BASE/"app"/"static", html=True), name="static")
