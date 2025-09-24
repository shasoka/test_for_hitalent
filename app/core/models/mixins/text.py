"""Модуль, содержащий примесь для создания текстовых полей."""

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column


class TextMixin:
    """Класс-примесь для создания текстовых полей."""

    text: Mapped[str] = mapped_column(Text, nullable=False)
