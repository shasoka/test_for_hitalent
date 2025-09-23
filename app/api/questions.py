from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Question
from core.schemas import QuestionRead

from services.questions import get_questions_svc

__all__ = ("router",)

router = APIRouter()


@router.get("/", response_model=list[QuestionRead])
async def get_questions(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[Question]:
    return await get_questions_svc(session)
