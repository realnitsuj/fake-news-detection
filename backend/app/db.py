import os

from databases import Database
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, create_engine
from sqlalchemy.sql import func

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

#############################################
# MODELS
#############################################

files = Table(
    "files",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("file", String(50)),
    Column("name", String(50)),
    Column("description", String(200)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

#############################################
#############################################

# databases query builder
database = Database(DATABASE_URL)
