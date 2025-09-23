from typing import Annotated

from pydantic import PlainValidator

__all__ = ("TextMixin",)


def _check_if_value_is_not_blank(value: str) -> str:
    if len(value) < 1 or not value.strip():
        raise ValueError("field must be not blank")
    return value


class TextMixin:
    text: Annotated[str, PlainValidator(_check_if_value_is_not_blank)]
