from pydantic import BaseModel


class IntIdPkMixin(BaseModel):
    id: int
