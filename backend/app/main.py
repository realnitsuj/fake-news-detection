from fastapi import FastAPI

from app.api import files, ping

app = FastAPI()

app.include_router(ping.router, tags=["ping"])
app.include_router(files.router, prefix="/files", tags=["files"])
