import uuid

from pydantic import BaseModel

from core.schemas.mixins import CreatedAtMixin, IntIdPkMixin, TextMixin


class AnswerRead(IntIdPkMixin, CreatedAtMixin, TextMixin, BaseModel):
    question_id: int
    user_id: uuid.UUID
