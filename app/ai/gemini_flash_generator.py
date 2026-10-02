from app.ai.gemini_client import generate_text
from app.config import settings


def generate_nutrition_tip_with_flash(
    goal: str
) -> str:

    if settings.mock_ai:

        return mock_tip(goal)


    prompt = f"""
Give one concise general nutrition
or recovery tip.

Fitness goal:

{goal}


Requirements:

- 2–4 sentences.
- Encourage balanced meals.
- Encourage hydration.
- Encourage adequate sleep.
- Avoid extreme calorie restriction.
- Do not provide medical treatment.
- Recommend professional advice for
  medical or nutrition concerns.
"""


    return generate_text(
        prompt,
        settings.gemini_nutrition_model,
        temperature=0.5
    )


def mock_tip(goal: str) -> str:

    tips = {

        "weight loss":
        """
Focus on balanced meals with vegetables,
protein, whole grains and enough fluids
rather than extreme restriction.
Consistent sleep and regular activity
also support general wellness.
""",

        "muscle gain":
        """
Include balanced sources of protein
in regular meals and stay hydrated.
Recovery, sleep and gradually increasing
activity are important parts of a
sustainable routine.
""",

        "general wellness":
        """
Aim for balanced meals, regular hydration,
adequate sleep and enjoyable physical
activity. Consistency is more useful
than extreme short-term changes.
""",

        "flexibility":
        """
Include a variety of nutritious foods
and enough fluids to support daily
activity. Gentle mobility work and
adequate recovery can complement
flexibility practice.
"""
    }


    return tips.get(
        goal,
        tips["general wellness"]
    ).strip()