"""Модуль, содержащий пользовательские валидаторы."""

import uuid

from typing import Any

__all__ = (
    "check_if_value_is_not_blank",
    "check_if_value_is_correct_uuid",
)


def check_if_value_is_not_blank(value: str) -> str:
    """
    Функция-валидатор для поля text.

    Проверяет строку на пустоту. Пустой считается строка длиной менее 1 символа
    или строка, состоящая только из пробелов.

    :param value: значение поля text;
    :return: значение поля text в случае успешной проверки, ValueError - в
             противном случае;
    """

    if len(value) < 1 or not value.strip():
        raise ValueError("поле 'text' не может быть пустым")
    return value


def check_if_value_is_correct_uuid(value: Any) -> uuid.UUID:
    """
    Функция-валидатор для поля user_id.

    Проверяет значение поля на соответствие формату uuid.

    :param value: значение поля user_id;
    :return: значение поля user_id в случае успешной проверки, ValueError - в
             противном случае;
    """

    try:
        return uuid.UUID(str(value))
    except (ValueError, TypeError):
        raise ValueError("поле 'user_id' должно быть корректным UUID")
