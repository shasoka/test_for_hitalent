"""Пакет, содержащий пользовательские классы-примеси для pydantic-схем."""

from app.core.schemas.mixins.created_at import CreatedAtMixin
from app.core.schemas.mixins.int_id_pk import IntIdPkMixin
from app.core.schemas.mixins.text import TextMixin

__all__ = (
    "CreatedAtMixin",
    "IntIdPkMixin",
    "TextMixin",
)
