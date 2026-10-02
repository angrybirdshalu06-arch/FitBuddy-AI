from app.ai.gemini_client import generate_text
from app.ai.gemini_generator import mock_workout
from app.config import settings


def update_workout_plan(
    original_plan: str,
    feedback: str,
    name: str,
    age: int,
    goal: str,
    intensity: str
) -> str:

    if settings.mock_ai:

        return (
            mock_workout(
                name,
                goal,
                intensity
            )
            +
            "\n\nUPDATE APPLIED FROM FEEDBACK:\n"
            +
            feedback
        )


    prompt = f"""
You are updating a FitBuddy
general wellness fitness plan.

User:

Name: {name}

Age: {age}

Goal: {goal}

Preferred intensity: {intensity}


ORIGINAL PLAN:

{original_plan}


USER FEEDBACK:

{feedback}


Create a complete revised 7-day plan.

Apply the user's useful feedback.

Keep useful parts of the original plan.

Use exactly 7 labeled days.

Each day should include:

Focus

Warm-up

Main workout

Cool-down/recovery


Do not prescribe:

- Extreme dieting
- Dehydration
- Unsafe exercise
- Medical treatment

If the feedback asks for something unsafe,
replace it with a safer alternative.

Return the complete revised plan.
"""


    return generate_text(
        prompt,
        settings.gemini_workout_model
    )