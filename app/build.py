from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, RedirectResponse

from core.config import settings


# from api import router as api_router
# from core.exceptions import register_exceptions_handlers
# from core.middlewares import register_middlewares
# from core.models import db_helper


# @asynccontextmanager
# async def lifespan(_app: FastAPI) -> AsyncGenerator[Any, Any]:
	# На __aenter__ ничего не происходит
	# После __aenter__ yield
	# yield
	# На __aexit__ dispose
	# await db_helper.dispose()


def build_app() -> FastAPI:
    app = FastAPI(
        default_response_class=ORJSONResponse,
        # lifespan=lifespan,
        title=settings.app.title,
        summary=settings.app.summary,
        description=settings.app.description,
        version=settings.app.version,
        swagger_ui_parameters=settings.app.swagger_ui_parameters,
        redoc_url=None,
    )

    # Редирект на документацию
    @app.get(settings.api.slash, include_in_schema=False)
    async def root():
        return RedirectResponse(url=settings.api.docs)

    # app.include_router(api_router)

    # register_exceptions_handlers(app)

    # register_middlewares(app)

    return app
