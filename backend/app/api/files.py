from fastapi import APIRouter, HTTPException

from app.api import crud
from app.api.models import FileSchema

router = APIRouter()


@router.post("/", status_code=201)
async def upload_file(payload: FileSchema):
    file_id = await crud.post(payload)
    return {"file_id": f"{file_id}"}


@router.get("/{id}/")
async def get_file():
    file = await crud.get(id)
    if not file:
        raise HTTPException(status_code=404, detail="Note not found")
    return file
