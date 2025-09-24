"""Модуль, содержащий примесь для создания первичного ключа."""

from sqlalchemy.orm import Mapped, mapped_column


class IntIdPkMixin:
    """Класс-примесь для создания первичного ключа."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
