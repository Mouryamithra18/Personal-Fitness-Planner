from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Mock AI Fitness Backend")

# Allow all origins for local testing (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserInput(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    existing_conditions: Optional[List[str]] = None
    physical_limitations: Optional[List[str]] = None
    doctor_approval: Optional[str] = None
    daily_steps: Optional[int] = 0
    heart_rate: Optional[int] = None
    calories_burned: Optional[int] = None
    sleep_duration: Optional[float] = None
    active_minutes: Optional[int] = None
    sedentary_minutes: Optional[int] = None
    goal: Optional[str] = None
    duration_pref: Optional[int] = None
    days_per_week: Optional[int] = None
    exercise_types: Optional[List[str]] = None


@app.post('/api/generate-plan')
async def generate_plan(user: UserInput):
    goal = (user.goal or '').lower()
    if 'weight' in goal:
        plan_type = 'weight_loss'
    elif 'strength' in goal or 'muscle' in goal:
        plan_type = 'strength'
    else:
        plan_type = 'balanced'

    base_steps = max(2000, min(12000, int(user.daily_steps or 4000)))
    step_goal = [base_steps + i * 500 for i in range(4)]
    base_cal = 1800
    calories_goal = [base_cal + i * 50 for i in range(4)]

    plan_text = {
        "Week 1": "Begin with mobility and low-impact cardio.",
        "Week 2": "Increase frequency and include strength/mobility sessions.",
        "Week 3": "Introduce higher intensity intervals or progressive overload.",
        "Week 4": "Taper, focus on recovery and flexibility." 
    }

    return {
        "plan_type": plan_type,
        "activity_level": "Moderate",
        "calories_target": calories_goal[-1],
        "step_goal": step_goal[-1],
        "rest_days": 2,
        "plan": plan_text,
        "weekly_targets": {
            "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "Steps Target": step_goal,
            "Calories Target": calories_goal,
        },
        "diet_plan": None
    }
