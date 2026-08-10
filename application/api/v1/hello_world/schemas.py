from pydantic import BaseModel, Field


class FilePathSchema(BaseModel):
    path: str


class FileContentSchema(FilePathSchema):
    content: str = Field(max_length=200)


## There is store for local uniq or repeatable shemas
