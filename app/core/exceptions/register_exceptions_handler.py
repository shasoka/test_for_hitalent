"""Модуль, содержащий функцию, регистрирующую обработчики исключений."""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from app.core.exceptions import NoEntityFoundException


def register_exceptions_handlers(app: FastAPI) -> None:
    """
    Функция, регистрирующая обработчики исключений.

    :param app: объект класса FastAPI.
    """

    # noinspection PyUnusedLocal
    @app.exception_handler(NoEntityFoundException)
    async def handle_no_entity_found_exception(
        request: Request,
        exc: NoEntityFoundException,
    ) -> ORJSONResponse:
        """
        Обработчик исключения NoEntityFoundException.

        :param request: запрос, вызвавший исключение;
        :param exc: вызванное исключение;
        :return: JSON-ответ с сообщением об ошибке.
        """

        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "Сущность не найдена",
                "error": str(exc),
            },
        )

    # noinspection PyUnusedLocal
    @app.exception_handler(RequestValidationError)
    async def handle_validation_error_exception(
        request: Request,
        exc: RequestValidationError,
    ) -> ORJSONResponse:
        """
        Обработчик исключения RequestValidationError.

        :param request: запрос, вызвавший исключение;
        :param exc: вызванное исключение;
        :return: JSON-ответ с сообщением об ошибке.
        """

        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Недопустимая сущность",
                "error": "; ".join([err["msg"] for err in exc.errors()]),
            },
        )
