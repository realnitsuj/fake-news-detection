from app.api.models import FileSchema
from app.db import database, files


async def post(payload: FileSchema):
    query = files.insert().values(title=payload.name, description=payload.description)
    return await database.execute(query=query)


async def get(id: int):
    query = files.select().where(id == files.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = files.select()
    return await database.fetch_all(query=query)
