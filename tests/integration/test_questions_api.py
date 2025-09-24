import uuid

import pytest
from httpx import ASGITransport, AsyncClient, Response
from sqlalchemy import Result as QueryResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.main import app
from app.core.models import Answer, Question


@pytest.mark.asyncio
class TestQuestionsAPI:

    @staticmethod
    async def _post_question(
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
        text: str,
    ) -> tuple[list[Question], list[Question], dict, int]:
        # Сохранение количества вопросов до добавления нового
        old_query_result: QueryResult = await db_session.execute(select(Question))
        old_db_questions: list[Question] = list(old_query_result.scalars().all())

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=base_url,
        ) as ac:
            # Выполнение запроса
            request_body: dict = {"text": text}
            response: Response = await ac.post(
                questions_prefix,
                json=request_body,
            )

        response_data: dict = response.json()
        new_query_result: QueryResult = await db_session.execute(select(Question))
        new_db_questions: list[Question] = list(new_query_result.scalars().all())

        return old_db_questions, new_db_questions, response_data, response.status_code

    async def _test_invalid_question_creation(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
        invalid_text: str,
        expected_error_message: str = "Недопустимая сущность",
    ) -> None:
        old_db_questions, new_db_questions, response_data, status_code = (
            await self._post_question(
                db_session=db_session,
                base_url=base_url,
                questions_prefix=questions_prefix,
                text=invalid_text,
            )
        )

        assert status_code == 422
        assert response_data["message"] == expected_error_message
        assert len(old_db_questions) == len(new_db_questions)

    async def test_get_all_questions_without_answers_200(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
    ) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=base_url,
        ) as ac:
            # Добавление вопроса в БД
            question: Question = Question(text="Question to get")
            db_session.add(question)
            await db_session.commit()
            await db_session.refresh(question)

            # Выполнение запроса
            response: Response = await ac.get(questions_prefix)

        # Проверка
        response_data: dict = response.json()
        query_result: QueryResult = await db_session.execute(select(Question))
        db_questions: list[Question] = list(query_result.scalars().all())

        assert response.status_code == 200
        assert response_data[0]["text"] == "Question to get"
        assert len(db_questions) == len(response_data) == 1

    async def test_create_question_200(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
    ) -> None:
        old_db_questions, new_db_questions, response_data, status_code = (
            await self._post_question(
                db_session=db_session,
                base_url=base_url,
                questions_prefix=questions_prefix,
                text="Question to create",
            )
        )

        assert status_code == 200
        assert response_data["text"] == new_db_questions[0].text == "Question to create"
        assert len(old_db_questions) + 1 == len(new_db_questions)

    async def test_create_question_422_text_field_is_empty(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
    ):
        await self._test_invalid_question_creation(
            db_session=db_session,
            base_url=base_url,
            questions_prefix=questions_prefix,
            invalid_text="",
        )

    async def test_create_question_422_text_field_consist_of_spaces(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
    ):
        await self._test_invalid_question_creation(
            db_session=db_session,
            base_url=base_url,
            questions_prefix=questions_prefix,
            invalid_text="",
        )

    async def test_get_question_with_answers_by_id_200(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=base_url,
        ) as ac:
            # Добавление вопроса и ответа в БД
            question: Question = Question(text="Question to get")
            db_session.add(question)
            await db_session.commit()
            await db_session.refresh(question)

            user_id: uuid.UUID = uuid.uuid4()
            answer: Answer = Answer(
                user_id=user_id,
                text="Answer to get",
                question_id=question.id,
            )
            db_session.add(answer)

            await db_session.commit()
            await db_session.refresh(question)

            # Выполнение запроса
            response: Response = await ac.get(questions_prefix + f"{question.id}")

        # Проверка
        response_data: dict = response.json()
        query_result: QueryResult = await db_session.execute(
            select(Question)
            .where(Question.id == question.id)
            .options(selectinload(Question.answers))
        )
        db_question: Question | None = query_result.scalar_one_or_none()

        assert response.status_code == 200
        assert db_question is not None
        assert db_question.text == response_data["text"] == "Question to get"
        assert len(db_question.answers) == len(response_data["answers"]) == 1
        assert (
            db_question.answers[0].text
            == response_data["answers"][0]["text"]
            == "Answer to get"
        )
        assert (
            str(db_question.answers[0].user_id)
            == response_data["answers"][0]["user_id"]
            == str(user_id)
        )

    async def test_get_question_with_answers_by_id_404(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=base_url,
        ) as ac:
            # Выполнение запроса
            response: Response = await ac.get(questions_prefix + "0")

        # Проверка
        response_data: dict = response.json()
        query_result: QueryResult = await db_session.execute(
            select(Question)
            .where(Question.id == 0)
            .options(selectinload(Question.answers))
        )
        db_question: Question | None = query_result.scalar_one_or_none()

        assert response.status_code == 404
        assert db_question is None
        assert response_data["message"] == "Сущность не найдена"
