from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def pong():
    # some async operation could happen here
    # example: `files = await get_all_files()`
    return {"ping": "pong!"}
