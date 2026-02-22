"""
READ THE FOLLOWING :
    https://fastapi.tiangolo.com/tutorial/request-files/
    https://fastapi.tiangolo.com/tutorial/request-forms-and-files/

"""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.api.models import FileSchema

router = APIRouter()


@router.post("/", status_code=201)
async def upload_file(payload: FileSchema):
    file_id = await crud.post(payload)
    return {"file_id": f"{file_id}"}


@router.get("/")
async def get_all_files():
    files = await crud.get_all()
    return {"files": files}


# https://fastapi.tiangolo.com/tutorial/path-params/
# https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/
@router.get("/{id}/")
async def get_file(
    id: Annotated[int, Path(title="The ID of the file to get", ge=0, le=1000)],
):
    file = await crud.get(id)
    if not file:
        raise HTTPException(status_code=404, detail="Note not found")
    return file
