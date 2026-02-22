from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def pong():
    return {"ping": "pong!"}


@router.get("/")
async def health_check():
    # A simple endpoint to confirm the server is running.
    return {"status": "ok"}
