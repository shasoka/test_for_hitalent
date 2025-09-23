from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Question
from crud.questions import get_questions_from_db

__all__ = ("get_questions_svc",)


async def get_questions_svc(session: AsyncSession) -> list[Question]:
    return await get_questions_from_db(session)
