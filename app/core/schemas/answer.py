import uuid
from typing import Annotated

from pydantic import BaseModel, PlainValidator

from core.schemas.mixins import CreatedAtMixin, IntIdPkMixin, TextMixin
from core.schemas.validators import check_if_value_is_correct_uuid


class AnswerBase(TextMixin, BaseModel):
    user_id: Annotated[uuid.UUID, PlainValidator(check_if_value_is_correct_uuid)]


class AnswerRead(IntIdPkMixin, CreatedAtMixin, AnswerBase):
    question_id: int


class AnswerCreate(AnswerBase):
    pass
