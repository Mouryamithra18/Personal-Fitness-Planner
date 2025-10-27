from typing import Dict


def generate_mock_plan(user_input: dict) -> dict:
    base_steps = max(2000, min(12000, int(user_input.get("daily_steps", 4000))))
    step_goal = [base_steps + i * 500 for i in range(4)]
    base_cal = 1800
    calories_goal = [base_cal + i * 50 for i in range(4)]
    plan_text = {
        "Week 1": "Light to moderate activity focusing on mobility and low-impact cardio.",
        "Week 2": "Increase intensity; add 1-2 strength sessions.",
        "Week 3": "Introduce interval work and slightly longer cardio sessions.",
        "Week 4": "Taper and focus on recovery + flexibility."
    }
    return {
        "activity_level": "Moderate",
        "calories_target": calories_goal[-1],
        "step_goal": step_goal[-1],
        "rest_days": 2,
        "plan": plan_text,
        "plan_type": ("weight_loss" if user_input.get('goal') == 'Weight loss' else "balanced"),
        "diet_plan": None,
        "weekly_targets": {
            "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "Steps Target": step_goal,
            "Calories Target": calories_goal,
        }
    }


def generate_diet_plan(plan_type: str, user_input: dict, calories_target: int) -> Dict:
    pt = (plan_type or "balanced").lower()
    meals = {}
    for d in range(1, 8):
        day = f"Day {d}"
        if pt == "weight_loss":
            cal = max(1200, int(calories_target * 0.85))
            meals[day] = [
                {"meal": "Breakfast", "cal": int(cal * 0.25), "suggestion": "Oatmeal with berries and a boiled egg"},
                {"meal": "Lunch", "cal": int(cal * 0.35), "suggestion": "Grilled chicken salad with mixed greens"},
                {"meal": "Dinner", "cal": int(cal * 0.30), "suggestion": "Steamed fish with vegetables"},
                {"meal": "Snack", "cal": int(cal * 0.10), "suggestion": "Greek yogurt or a small handful of nuts"}
            ]
        elif pt == "strength" or pt == "muscle_gain":
            cal = int(calories_target * 1.1)
            meals[day] = [
                {"meal": "Breakfast", "cal": int(cal * 0.25), "suggestion": "Scrambled eggs, wholegrain toast, banana"},
                {"meal": "Lunch", "cal": int(cal * 0.30), "suggestion": "Quinoa bowl with chicken and veggies"},
                {"meal": "Dinner", "cal": int(cal * 0.30), "suggestion": "Beef or tofu stir-fry with brown rice"},
                {"meal": "Snack", "cal": int(cal * 0.15), "suggestion": "Protein shake or cottage cheese"}
            ]
        else:
            cal = int(calories_target)
            meals[day] = [
                {"meal": "Breakfast", "cal": int(cal * 0.25), "suggestion": "Greek yogurt with granola and fruit"},
                {"meal": "Lunch", "cal": int(cal * 0.30), "suggestion": "Turkey sandwich and salad"},
                {"meal": "Dinner", "cal": int(cal * 0.30), "suggestion": "Grilled salmon with quinoa and veggies"},
                {"meal": "Snack", "cal": int(cal * 0.15), "suggestion": "Fruit or a small handful of nuts"}
            ]

    return {"plan_type": pt, "calories_target": calories_target, "meals": meals}
