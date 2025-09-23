from datetime import datetime

from pydantic import BaseModel


class CreatedAtMixin(BaseModel):
    created_at: datetime
