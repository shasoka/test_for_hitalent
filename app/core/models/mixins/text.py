from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column


class TextMixin:
    text: Mapped[str] = mapped_column(Text, nullable=False)
