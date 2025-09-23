import uuid

__all__ = (
    "check_if_value_is_not_blank",
    "check_if_value_is_correct_uuid",
)


def check_if_value_is_not_blank(value: str) -> str:
    if len(value) < 1 or not value.strip():
        raise ValueError("поле 'text' не может быть пустым")
    return value


def check_if_value_is_correct_uuid(value: uuid.UUID) -> uuid.UUID:
    try:
        return uuid.UUID(str(value))
    except (ValueError, TypeError):
        raise ValueError("поле 'user_id' должно быть корректным UUID")
