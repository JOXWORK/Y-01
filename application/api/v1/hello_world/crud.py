"""
Create
Read
Update
Delete
"""

from __future__ import annotations

from os import remove as file_remove
from random import choice
from string import ascii_letters, digits
from typing import TYPE_CHECKING

import httpx
from core.models.example import Example
from core.tasks import for_loop_task_example_task

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from taskiq.result.result import TaskiqResult


def create_file(path: str, content: str) -> bool:
    with open(path, "w") as file:
        file.write(content)
    return True


def read_file(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


def update_file(path: str, content: str) -> bool:
    with open(path, "a") as file:
        file.write(content)

    return True


def delete_file(path: str) -> bool:
    file_remove(path)
    return True


def generate_random_string(length: int = 4) -> str:
    characters = ascii_letters + digits
    random_string = "".join([choice(characters) for i in range(length)])
    return random_string


async def create_row_example(random_string_generation: bool, session: AsyncSession) -> None:
    write_string = random_string_generation and generate_random_string(4) or "example"
    some_example = Example(example=write_string)

    session.add(some_example)
    await session.commit()


async def get_row_example(id: int, session: AsyncSession) -> Example:
    return await session.get(
        entity=Example,
        ident=id,
    )


async def for_loop_task_example(stop: int) -> TaskiqResult:
    task = await for_loop_task_example_task.kiq(stop)
    result = await task.wait_result()

    return result


async def httpbin_get_request() -> str:
    url = "https://httpbin.org/get"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=url,
            timeout=30,
        )

        return response.text
