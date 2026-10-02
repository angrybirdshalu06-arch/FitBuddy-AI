from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.ai.gemini_client import GeminiServiceError

from app.ai.gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)

from app.ai.gemini_generator import (
    generate_workout_gemini
)

from app.ai.updated_plan import (
    update_workout_plan
)

from app.database import get_db

from app.models import User
from app.models import WorkoutPlan

from app.schemas import FeedbackRequest
from app.schemas import PlanResponse
from app.schemas import UserInput


router = APIRouter(
    prefix="/api",
    tags=["FitBuddy API"]
)


def validate_minor_goal(
    data: UserInput
):

    if data.age < 18:

        if data.goal != "general wellness":

            raise HTTPException(

                status_code=422,

                detail=
                "For users under 18, this demo "
                "supports the general wellness "
                "goal only."
            )


def serialize_plan(
    user: User,
    updated: bool = False
) -> PlanResponse:

    plan = user.plan

    assert plan is not None


    workout = plan.original_plan

    nutrition = (
        plan.original_nutrition_tip
    )


    if updated and plan.updated_plan:

        workout = plan.updated_plan

        nutrition = (
            plan.updated_nutrition_tip
            or nutrition
        )


    return PlanResponse(

        user_id=user.user_id,

        name=user.name,

        age=user.age,

        weight_kg=user.weight_kg,

        goal=user.goal,

        intensity=user.intensity,

        workout_plan=workout,

        nutrition_tip=nutrition,

        updated=(
            updated
            and bool(plan.updated_plan)
        )
    )


@router.post(
    "/plans",
    response_model=PlanResponse
)
def create_plan(

    data: UserInput,

    db: Session = Depends(get_db)
):

    validate_minor_goal(data)


    try:

        user = (
            db.query(User)
            .filter(
                User.user_id == data.user_id
            )
            .first()
        )


        if user is None:

            user = User(
                **data.model_dump()
            )

            db.add(user)

            db.flush()


        else:

            for key, value in (
                data.model_dump().items()
            ):

                setattr(
                    user,
                    key,
                    value
                )


        workout = generate_workout_gemini(

            data.name,

            data.age,

            data.weight_kg,

            data.goal,

            data.intensity
        )


        tip = generate_nutrition_tip_with_flash(
            data.goal
        )


        if user.plan is None:

            user.plan = WorkoutPlan(

                original_plan=workout,

                original_nutrition_tip=tip
            )


        else:

            user.plan.original_plan = workout

            user.plan.original_nutrition_tip = tip

            user.plan.updated_plan = None

            user.plan.updated_nutrition_tip = None

            user.plan.feedback = None


        db.commit()

        db.refresh(user)


        return serialize_plan(user)


    except GeminiServiceError as exc:

        db.rollback()

        raise HTTPException(

            status_code=502,

            detail=str(exc)
        ) from exc


@router.post(
    "/plans/{user_id}/feedback",
    response_model=PlanResponse
)
def update_plan_endpoint(

    user_id: str,

    request: FeedbackRequest,

    db: Session = Depends(get_db)
):

    if user_id != request.user_id:

        raise HTTPException(

            status_code=400,

            detail=
            "Path user_id and body user_id "
            "must match."
        )


    user = (
        db.query(User)
        .filter(
            User.user_id == user_id
        )
        .first()
    )


    if user is None or user.plan is None:

        raise HTTPException(

            status_code=404,

            detail="User or plan not found."
        )


    try:

        revised = update_workout_plan(

            user.plan.original_plan,

            request.feedback,

            user.name,

            user.age,

            user.goal,

            user.intensity
        )


        tip = generate_nutrition_tip_with_flash(
            user.goal
        )


        user.plan.updated_plan = revised

        user.plan.updated_nutrition_tip = tip

        user.plan.feedback = request.feedback


        db.commit()

        db.refresh(user)


        return serialize_plan(
            user,
            updated=True
        )


    except GeminiServiceError as exc:

        db.rollback()

        raise HTTPException(

            status_code=502,

            detail=str(exc)
        ) from exc


@router.get(
    "/users/{user_id}",
    response_model=PlanResponse
)
def get_user(

    user_id: str,

    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.user_id == user_id
        )
        .first()
    )


    if user is None or user.plan is None:

        raise HTTPException(

            status_code=404,

            detail="User or plan not found."
        )


    return serialize_plan(

        user,

        updated=bool(
            user.plan.updated_plan
        )
    )