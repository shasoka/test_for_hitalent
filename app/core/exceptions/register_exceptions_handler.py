from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from core.exceptions import NoEntityFoundException


def register_exceptions_handlers(app: FastAPI) -> None:

    # noinspection PyUnusedLocal
    @app.exception_handler(NoEntityFoundException)
    async def handle_no_entity_found_exception(
        request: Request,
        exc: NoEntityFoundException,
    ) -> ORJSONResponse:
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
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Недопустимая сущность",
                "error": "; ".join([err["msg"] for err in exc.errors()]),
            },
        )
