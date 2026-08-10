from os import path as os_path

from fastapi import HTTPException, status

from .crud import create_file
from .schemas import FileContentSchema, FilePathSchema


def create_file_depends(file_schema: FileContentSchema) -> bool:
    exists = os_path.exists(path=file_schema.path)
    if exists:
        return False
    else:
        created = create_file(path=file_schema.path, content=file_schema.content)
        return created


def check_file_exists(path_schema: FilePathSchema) -> bool:
    path = path_schema.path
    exists = os_path.exists(path=path)
    if exists:
        return path
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )


def check_exists_and_get_content(file_schema: FileContentSchema) -> tuple[str, str]:
    path = file_schema.path
    if os_path.exists(path=path):
        content = file_schema.content
        return path, content
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
