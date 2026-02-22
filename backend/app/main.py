from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import files, ping

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ping.router, tags=["ping"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(files.router, prefix="/ai", tags=["ai"])
