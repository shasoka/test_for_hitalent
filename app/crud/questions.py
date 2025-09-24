"""Модуль, содержащий CRUD-операции сущности Question."""

from typing import Sequence

from sqlalchemy import Result as QueryResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NoEntityFoundException
from app.core.models import Question
from app.core.schemas import QuestionCreate

__all__ = (
    "create_question_in_db",
    "delete_question_in_db",
    "get_questions_from_db",
    "get_question_with_answers_from_db",
    "get_question_by_id",
)


async def get_question_by_id(
    session: AsyncSession,
    question_id: int,
) -> Question:
    """
    Функция получения вопроса по его id.

    :param session: сессия подключения к БД;
    :param question_id: идентификатор вопроса;
    :return: полученный объект Question.
    """

    query_result: QueryResult = await session.execute(
        select(Question).where(Question.id == question_id)
    )
    question: Question | None = query_result.scalar_one_or_none()
    return question


async def get_questions_from_db(session: AsyncSession) -> list[Question]:
    """
    Функция получения всех вопросов.

    :param session: сессия подключения к БД;
    :return: список объектов Question.
    """

    query_result: QueryResult = await session.execute(select(Question))
    questions: Sequence[Question] = query_result.scalars().all()
    return list(questions)


async def get_question_with_answers_from_db(
    question_id: int,
    session: AsyncSession,
) -> Question:
    """
    Функция получения вопроса и ответов на него по его идентификатору.

    :param question_id: идентификатор вопроса;
    :param session: сессия подключения к БД;
    :return: объект типа Question и связанные с ним объекты типа Answer.
    """

    query_result: QueryResult = await session.execute(
        select(Question)
        .where(Question.id == question_id)
        .options(selectinload(Question.answers))
    )
    question: Question = query_result.scalar_one_or_none()
    return question


async def create_question_in_db(
    session: AsyncSession,
    question_in: QuestionCreate,
) -> Question:
    """
    Функция создания записи в таблице questions.

    :param session: сессия подключения к БД.
    :param question_in: объект типа QuestionCreate, полученный из тела запроса;
    :return: созданный объект типа Question.
    """

    question = Question(**question_in.dict())
    session.add(question)
    await session.commit()
    return question


async def delete_question_in_db(
    session: AsyncSession,
    question_to_delete: Question,
) -> Question:
    """
    Функция удаления записи из таблицы questions.

    :param session: сессия подключения к БД;
    :param question_to_delete: объект типа Question, который будет удален;
    :return: удаленный объект типа Question.
    """

    await session.delete(question_to_delete)
    await session.commit()
    return question_to_delete
