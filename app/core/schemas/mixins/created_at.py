"""Модуль, содержащий примесь для создания полей-меток времени."""

from datetime import datetime


class CreatedAtMixin:
    """Класс-примесь для создания полей-меток времени."""

    created_at: datetime
