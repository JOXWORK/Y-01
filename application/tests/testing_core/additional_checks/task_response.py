from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest
from api.schemas.v1.api_task_response import APITaskResponseSchema
from api.schemas.v1.task_id import TaskIDSchema
from pydantic import ValidationError

from tests.testing_core.test_depends import test_depends

if TYPE_CHECKING:
    from httpx import AsyncClient
    from pydantic import BaseModel


async def class_task_response_check(
    class_db_auth_header: dict,
    class_httpx_client: AsyncClient,
    response_content: bytes,
    validation_model: BaseModel | None = None,
    *,
    retries: int = 3,
    delay: int = 2,
):
    task_id_schema = TaskIDSchema.model_validate_json(response_content)

    for _ in range(retries):
        response = await class_httpx_client.get(
            url=test_depends.urls.task_response(f"/get/{task_id_schema.task_id}"),
            headers=class_db_auth_header,
        )
        assert response.status_code == 200

        task_response_schema = APITaskResponseSchema.model_validate_json(response.content)
        if not task_response_schema.ready:
            await asyncio.sleep(delay)
            continue
        assert task_response_schema.successful

        task_content = task_response_schema.content

        if validation_model is None:
            if task_content is not None:
                pytest.fail(f"Validation model is None, but task response content does not: {task_content}")

            return

        try:
            return validation_model.model_validate(task_content)
        except ValidationError as exc:
            pytest.fail(f"Validation by model {validation_model} got error: {exc}")

    pytest.fail("Task response does not ready too long")
