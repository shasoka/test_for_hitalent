from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Answer
from core.schemas import AnswerCreate
from crud.answers import create_answer_in_db

__all__ = ("create_answer_svc",)


async def create_answer_svc(
    session: AsyncSession,
    question_id: int,
    answer_in: AnswerCreate,
) -> Answer:
    return await create_answer_in_db(session, question_id, answer_in)
