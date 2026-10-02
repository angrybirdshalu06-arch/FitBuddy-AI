from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


Goal = Literal[
    "weight loss",
    "muscle gain",
    "general wellness",
    "flexibility"
]


Intensity = Literal[
    "low",
    "medium",
    "high"
]


class UserInput(BaseModel):

    user_id: str = Field(
        min_length=2,
        max_length=64
    )

    name: str = Field(
        min_length=2,
        max_length=100
    )

    age: int = Field(
        ge=13,
        le=100
    )

    weight_kg: float = Field(
        gt=20,
        lt=400
    )

    goal: Goal

    intensity: Intensity

    @field_validator(
        "user_id",
        "name"
    )
    @classmethod
    def clean_text(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Value cannot be empty."
            )

        return value


class FeedbackRequest(BaseModel):

    user_id: str = Field(
        min_length=2,
        max_length=64
    )

    feedback: str = Field(
        min_length=5,
        max_length=1000
    )

    @field_validator("feedback")
    @classmethod
    def clean_feedback(cls, value: str) -> str:

        return value.strip()


class PlanResponse(BaseModel):

    user_id: str

    name: str

    age: int

    weight_kg: float

    goal: str

    intensity: str

    workout_plan: str

    nutrition_tip: str

    updated: bool = False