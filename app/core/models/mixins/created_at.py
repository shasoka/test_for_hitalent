"""Модуль, содержащий примесь для создания полей-меток времени."""

from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


def get_current_dt() -> datetime:
    """
    Функция, возвращающая текущее время в UTC+0 без tzinfo.

    :return: текущее время в UTC+0 без tzinfo.
    """

    dt: datetime = datetime.now(tz=timezone.utc)
    return dt.replace(tzinfo=None)


class CreatedAtMixin:
    """Класс-примесь с полем-меткой времени."""

    created_at: Mapped[datetime] = mapped_column(
        default=get_current_dt,
        server_default=func.now(),
    )
