import pytest
from httpx import ASGITransport, AsyncClient, Response
from sqlalchemy import Result as QueryResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.core.models import Question


@pytest.mark.asyncio
class TestQuestionsAPI:

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
        # Сохранение количества вопросов до добавления нового
        old_query_result: QueryResult = await db_session.execute(select(Question))
        old_db_questions: list[Question] = list(old_query_result.scalars().all())

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=base_url,
        ) as ac:
            # Выполнение запроса
            request_body: dict = {"text": "Question to create"}
            response: Response = await ac.post(
                questions_prefix,
                json=request_body,
            )

        response_data: dict = response.json()
        new_query_result: QueryResult = await db_session.execute(select(Question))
        new_db_questions: list[Question] = list(new_query_result.scalars().all())

        assert response.status_code == 200
        assert response_data["text"] == new_db_questions[0].text == "Question to create"
        assert len(old_db_questions) + 1 == len(new_db_questions)
