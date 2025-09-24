"""Пакет, содержащий пользовательские исключения."""

from app.core.exceptions.db_exceptions import NoEntityFoundException
from app.core.exceptions.register_exceptions_handler import register_exceptions_handlers

__all__ = ("NoEntityFoundException", "register_exceptions_handlers")
