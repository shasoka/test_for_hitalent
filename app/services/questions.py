"""Модуль, содержащий бизнес-логику, связанную с сущностью Question."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NoEntityFoundException
from app.core.models import Question
from app.core.schemas import QuestionCreate
from app.crud.questions import (
    create_question_in_db,
    delete_question_in_db,
    get_question_with_answers_from_db,
    get_questions_from_db,
    get_question_by_id,
)

__all__ = (
    "get_questions_svc",
    "get_question_with_answers_svc",
    "create_question_svc",
    "delete_question_svc",
)


async def get_questions_svc(session: AsyncSession) -> list[Question]:
    """
    Функция, возвращающая список всех вопросов в БД.

    :param session: сессия подключения к БД;
    :return: полученный список вопросов.
    """

    return await get_questions_from_db(session=session)


async def get_question_with_answers_svc(
    question_id: int,
    session: AsyncSession,
) -> Question:
    """
    Функция получения вопроса и связанных с ним ответов по его идентификатору.
    В случае, если вопрос не найден, выбрасывается исключение
    NoEntityFoundException.

    :param question_id: идентификатор вопроса;
    :param session: сессия подключения к БД;
    :return: найденный объект типа Question и связанные с ним объекты типа
             Answer.
    """

    if question := (
        await get_question_with_answers_from_db(
            session=session,
            question_id=question_id,
        )
    ):
        return question
    raise NoEntityFoundException(f"Вопрос с id={question_id} не найден в БД")


async def create_question_svc(
    session: AsyncSession,
    question_in: QuestionCreate,
) -> Question:
    """
    Функция создания вопроса.

    :param session: сессия подключения к БД;
    :param question_in: объект типа QuestionCreate, полученный из тела запроса;
    :return: созданный объект Question.
    """

    return await create_question_in_db(
        session=session,
        question_in=question_in,
    )


async def delete_question_svc(
    session: AsyncSession,
    question_id: int,
) -> Question:
    """
        Функция удаления вопроса по его идентификатору.
        В случае, если вопрос не найден, выбрасывается исключение
    NoEntityFoundException.

    :param session: сессия подключения к БД;
    :param question_id: идентификатор вопроса;
    :return: удаленный объект Question.
    """

    if question_to_delete := (
        await get_question_by_id(
            session=session,
            question_id=question_id,
        )
    ):
        return await delete_question_in_db(
            session=session,
            question_to_delete=question_to_delete,
        )
    raise NoEntityFoundException(f"Вопрос с id={question_id} не найден в БД")
