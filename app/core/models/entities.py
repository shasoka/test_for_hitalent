import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base
from app.core.models.mixins import CreatedAtMixin, IntIdPkMixin, TextMixin


class Question(IntIdPkMixin, TextMixin, CreatedAtMixin, Base):
    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan",
    )


class Answer(IntIdPkMixin, TextMixin, CreatedAtMixin, Base):
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    question_id: Mapped[int] = mapped_column(
        ForeignKey(
            "questions.id",
            ondelete="CASCADE",
        ),
    )

    question: Mapped["Question"] = relationship(
        "Question",
        back_populates="answers",
    )
