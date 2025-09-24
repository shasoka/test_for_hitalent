from pydantic import BaseModel

from app.core.schemas.answer import AnswerRead
from app.core.schemas.mixins import CreatedAtMixin, IntIdPkMixin, TextMixin


class QuestionBase(TextMixin, BaseModel):
    pass


class QuestionRead(IntIdPkMixin, CreatedAtMixin, QuestionBase):
    pass


class QuestionWithAnswersRead(QuestionRead):
    answers: list[AnswerRead]


class QuestionCreate(QuestionBase):
    pass
