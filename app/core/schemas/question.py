from pydantic import BaseModel

from .mixins import CreatedAtMixin, IntIdPkMixin, TextMixin


class QuestionBase(TextMixin, CreatedAtMixin, BaseModel):
    pass


class QuestionRead(IntIdPkMixin, QuestionBase):
    pass
