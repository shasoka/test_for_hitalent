from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Answer
from app.core.schemas import AnswerCreate
from app.crud.answers import (
    create_answer_in_db,
    delete_answer_in_db,
    get_answer_by_id_or_404,
)

__all__ = ("create_answer_svc", "get_answer_by_id_svc")


async def create_answer_svc(
    session: AsyncSession,
    answer_id: int,
    answer_in: AnswerCreate,
) -> Answer:
    return await create_answer_in_db(session, answer_id, answer_in)


async def get_answer_by_id_svc(
    answer_id: int,
    session: AsyncSession,
):
    return await get_answer_by_id_or_404(session, answer_id)


async def delete_answer_svc(
    answer_id: int,
    session: AsyncSession,
) -> Answer:
    return await delete_answer_in_db(session, answer_id)
