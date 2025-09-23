from pydantic import BaseModel


class TextMixin(BaseModel):
    text: str
