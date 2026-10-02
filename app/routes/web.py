from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

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

from app.config import settings

from app.database import get_db

from app.models import User
from app.models import WorkoutPlan

from app.schemas import UserInput


router = APIRouter()


templates = Jinja2Templates(
    directory="templates"
)


def validate_user(data: UserInput):

    if data.age < 18:

        if data.goal != "general wellness":

            raise ValueError(
                "For users under 18, this demo "
                "supports the general wellness "
                "goal only."
            )


@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={
            "error": None,
            "settings": settings
        }
    )


@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(

    request: Request,

    user_id: str = Form(...),

    name: str = Form(...),

    age: int = Form(...),

    weight_kg: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    db: Session = Depends(get_db)
):

    try:

        data = UserInput(

            user_id=user_id,

            name=name,

            age=age,

            weight_kg=weight_kg,

            goal=goal,

            intensity=intensity
        )


        validate_user(data)


        user = (
            db.query(User)
            .filter(
                User.user_id == data.user_id
            )
            .first()
        )


        if user is None:

            user = User(

                user_id=data.user_id,

                name=data.name,

                age=data.age,

                weight_kg=data.weight_kg,

                goal=data.goal,

                intensity=data.intensity
            )

            db.add(user)

            db.flush()


        else:

            user.name = data.name

            user.age = data.age

            user.weight_kg = data.weight_kg

            user.goal = data.goal

            user.intensity = data.intensity


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


        return templates.TemplateResponse(

            request=request,

            name="result.html",

            context={

                "user": user,

                "plan": user.plan,

                "message": None,

                "error": None
            }
        )


    except (
        ValueError,
        GeminiServiceError
    ) as exc:

        db.rollback()


        return templates.TemplateResponse(

            request=request,

            name="error.html",

            context={
                "message": str(exc)
            },

            status_code=400
        )


@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(

    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.user_id == user_id.strip()
        )
        .first()
    )


    if user is None or user.plan is None:

        return templates.TemplateResponse(

            request=request,

            name="error.html",

            context={
                "message":
                "User or workout plan was not found."
            },

            status_code=404
        )


    try:

        feedback = feedback.strip()


        if len(feedback) < 5:

            raise ValueError(
                "Feedback must contain at least 5 characters."
            )


        if len(feedback) > 1000:

            raise ValueError(
                "Feedback must be 1000 characters or fewer."
            )


        revised = update_workout_plan(

            user.plan.original_plan,

            feedback,

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

        user.plan.feedback = feedback


        db.commit()


        return templates.TemplateResponse(

            request=request,

            name="result.html",

            context={

                "user": user,

                "plan": user.plan,

                "message":
                "Your plan was updated using the feedback.",

                "error": None
            }
        )


    except (
        ValueError,
        GeminiServiceError
    ) as exc:

        db.rollback()


        return templates.TemplateResponse(

            request=request,

            name="error.html",

            context={
                "message": str(exc)
            },

            status_code=400
        )


@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(

    request: Request,

    admin_key: str = "",

    db: Session = Depends(get_db)
):

    if admin_key != settings.admin_key:

        return templates.TemplateResponse(

            request=request,

            name="error.html",

            context={
                "message":
                "Invalid admin key."
            },

            status_code=403
        )


    users = (
        db.query(User)
        .order_by(
            User.created_at.desc()
        )
        .all()
    )


    return templates.TemplateResponse(

        request=request,

        name="all_users.html",

        context={
            "users": users
        }
    )