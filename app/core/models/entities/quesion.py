from core.models.base import Base
from core.models.mixins import CreatedAtMixin, IntIdPkMixin, TextMixin


class Question(IntIdPkMixin, TextMixin, CreatedAtMixin, Base):
    pass
