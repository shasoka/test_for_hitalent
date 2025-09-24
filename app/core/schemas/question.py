"""Модуль, содержащий pydantic-схемы для сущности Question."""

from pydantic import BaseModel

from app.core.schemas.answer import AnswerRead
from app.core.schemas.mixins import CreatedAtMixin, IntIdPkMixin, TextMixin


class QuestionBase(TextMixin, BaseModel):
    """Базовая pydantic-схема для Question."""

    pass


class QuestionRead(IntIdPkMixin, CreatedAtMixin, QuestionBase):
    """Pydantic-схема для чтения Question."""

    pass


class QuestionWithAnswersRead(QuestionRead):
    """Pydantic-схема для чтения Question с ответами."""

    answers: list[AnswerRead]


class QuestionCreate(QuestionBase):
    """Pydantic-схема для создания Question."""

    pass
