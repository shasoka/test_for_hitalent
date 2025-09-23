from pydantic import BaseModel

from .answer import AnswerRead
from .mixins import CreatedAtMixin, IntIdPkMixin, TextMixin


class QuestionBase(TextMixin, BaseModel):
    pass


class QuestionRead(IntIdPkMixin, CreatedAtMixin, QuestionBase):
    pass


class QuestionWithAnswersRead(QuestionRead):
    answers: list[AnswerRead]


class QuestionCreate(QuestionBase):
    pass
