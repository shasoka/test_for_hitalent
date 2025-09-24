from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from app.core.config import settings


def _camel_case_to_snake_case(input_str: str) -> str:
    chars = []
    for idx, char in enumerate(input_str):
        if idx and char.isupper():
            nxt_idx = idx + 1
            flag = nxt_idx >= len(input_str) or input_str[nxt_idx].isupper()
            prev_char = input_str[idx - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                chars.append("_")
        chars.append(char.lower())
    return "".join(chars)


class Base(DeclarativeBase):
    """Базовый класс сущностей."""

    __abstract__ = True

    metadata = MetaData(naming_convention=settings.db.naming_convention)

    # noinspection PyMethodParameters
    @declared_attr.directive
    def __tablename__(cls):
        return f"{_camel_case_to_snake_case(cls.__name__)}s"
