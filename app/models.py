from datetime import datetime
from datetime import timezone

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database import Base


def utc_now() -> datetime:

    return datetime.now(timezone.utc)


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    weight_kg: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    goal: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    intensity: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now
    )

    plan: Mapped["WorkoutPlan | None"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False
    )


class WorkoutPlan(Base):

    __tablename__ = "workout_plans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    original_plan: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    original_nutrition_tip: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    updated_plan: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    updated_nutrition_tip: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now
    )

    user: Mapped[User] = relationship(
        back_populates="plan"
    )