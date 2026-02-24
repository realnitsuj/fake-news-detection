import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ai, files, ping

# Configure basic logging
# https://betterstack.com/community/guides/logging/logging-with-fastapi/
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a logger instance
logger = logging.getLogger(__name__)

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
app.include_router(ai.router, prefix="/ai", tags=["ai"])
