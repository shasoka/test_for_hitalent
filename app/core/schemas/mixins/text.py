from typing import Annotated

from pydantic import PlainValidator

from app.core.schemas.validators import check_if_value_is_not_blank

__all__ = ("TextMixin",)


class TextMixin:
    text: Annotated[str, PlainValidator(check_if_value_is_not_blank)]
