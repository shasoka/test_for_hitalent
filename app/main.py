import uvicorn
from fastapi import FastAPI

from build import build_app
from core.config import settings

app: FastAPI = build_app()

if __name__ == "__main__":
    uvicorn.run(
        app=settings.run.app_location,
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
