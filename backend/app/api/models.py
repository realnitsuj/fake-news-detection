from pydantic import BaseModel, Field


class FileSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class TextSchema(BaseModel):
    text: str = Field(..., min_length=50, max_length=500)
