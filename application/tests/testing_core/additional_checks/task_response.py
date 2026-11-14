import asyncio
from typing import TypeVar

import pytest
from api.schemas.v1.api_task_response import APITaskResponseSchema
from api.schemas.v1.task_id import TaskIDSchema
from httpx import AsyncClient
from pydantic import BaseModel, ValidationError

from tests.testing_core.test_depends import test_depends

TP_SCHEMA = TypeVar("VAL_SCHEMA", bound=BaseModel)


async def class_task_response_check(
    class_db_auth_header: dict,
    class_httpx_client: AsyncClient,
    response_content: bytes,
    validation_model: type[TP_SCHEMA] = None,
    *,
    retries: int = 3,
    delay: int = 2,
    unsuccessful_ok: bool = False,
) -> TP_SCHEMA:
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

        if not unsuccessful_ok:
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
