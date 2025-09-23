from fastapi import APIRouter

__all__ = ("router",)

router = APIRouter()


@router.get("/")
async def get_questions():
    return "Hello World"
