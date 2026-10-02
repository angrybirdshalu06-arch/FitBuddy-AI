from app.ai.gemini_client import generate_text
from app.config import settings


def generate_workout_gemini(
    name: str,
    age: int,
    weight_kg: float,
    goal: str,
    intensity: str
) -> str:

    if settings.mock_ai:

        return mock_workout(
            name,
            goal,
            intensity
        )


    prompt = f"""
You are FitBuddy, a general wellness planning assistant.

Create a safe and practical 7-day fitness plan.

User information:

Name: {name}

Age: {age}

Weight: {weight_kg} kg

Goal: {goal}

Preferred intensity: {intensity}


Requirements:

1. Create exactly 7 labeled days.

2. Each day should contain:
   - Focus
   - Warm-up
   - Main workout
   - Cool-down/recovery

3. Include exercises with sets,
   repetitions, or duration where appropriate.

4. Include rest or recovery days.

5. Keep the plan appropriate for a general
   wellness application.

6. Do not provide medical diagnosis.

7. Do not prescribe extreme dieting,
   dehydration, or unsafe exercise.

8. Tell the user to stop if an exercise
   causes pain.

9. Recommend qualified professional
   guidance for injuries or medical concerns.

10. Use simple readable text.

Do not use markdown tables.
"""


    return generate_text(
        prompt,
        settings.gemini_workout_model
    )


def mock_workout(
    name: str,
    goal: str,
    intensity: str
) -> str:

    return f"""
7-DAY FITBUDDY PLAN FOR {name.upper()}

Goal: {goal}

Intensity: {intensity}


DAY 1 — FULL BODY

Warm-up:
5–10 minutes of easy walking and mobility.

Main workout:
Bodyweight squats 2–3 x 10
Wall or incline push-ups 2–3 x 8
Glute bridges 2–3 x 12

Cool-down:
5 minutes of gentle stretching.


DAY 2 — CARDIO + MOBILITY

Warm-up:
5 minutes easy movement.

Main workout:
20–30 minutes comfortable walking
or another suitable low-impact activity.

Cool-down:
Gentle hip, shoulder and calf mobility.


DAY 3 — RECOVERY

Focus:
Easy walking and light mobility.

Recovery:
Keep activity comfortable and prioritize rest.


DAY 4 — FULL BODY

Warm-up:
5–10 minutes.

Main workout:
Reverse lunges 2 x 8 each side
Resistance-band rows 2–3 x 10
Bird-dog 2 x 8 each side

Cool-down:
5 minutes gentle stretching.


DAY 5 — CARDIO

Warm-up:
5 minutes.

Main workout:
20–30 minutes moderate,
comfortable cardio.

Cool-down:
Easy walking and breathing exercises.


DAY 6 — CORE + MOBILITY

Warm-up:
5 minutes.

Main workout:
Dead bug 2 x 8 each side
Plank 2 x 15–30 seconds
Controlled bodyweight movements 2 x 10

Cool-down:
Gentle stretching.


DAY 7 — REST / LIGHT ACTIVITY

Focus:
Rest, an easy walk, or gentle mobility.

Recovery:
Hydrate, sleep well and prepare
for the next week.


Safety note:
This is general wellness guidance,
not medical advice.
"""