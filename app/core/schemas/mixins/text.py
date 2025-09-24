"""Модуль, содержащий примесь для создания полей текста."""

from typing import Annotated

from pydantic import PlainValidator

from app.core.schemas.validators import check_if_value_is_not_blank


class TextMixin:
    """Класс-примесь для создания полей текста."""

    text: Annotated[str, PlainValidator(check_if_value_is_not_blank)]
