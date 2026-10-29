import asyncio

import pytest
from api.schemas.v1.api_task_response import APITaskResponseSchema
from core.schemas.moderation_rules import ModerationRulesSchema
from httpx import AsyncClient
from pydantic import ValidationError
from tests.testing_core.schemas.task_id_validation import TaskIDValidationSchema
from tests.testing_core.test_depends import test_depends


@pytest.mark.asyncio(loop_scope="class")
@pytest.mark.delay(3)
class TestModerationRules:
    async def test_create_rules(
        self,
        class_db_auth_header: dict,
        class_httpx_client: AsyncClient,
        moderation_rules: dict,
        func_class__async_delay,
    ):
        response = await class_httpx_client.post(
            url=test_depends.urls.rules("/create"),
            headers=class_db_auth_header,
            json=moderation_rules,
        )

        assert response.status_code == 200

    async def test_get_rules(self, class_db_auth_header: dict, class_httpx_client: AsyncClient):
        response = await class_httpx_client.post(
            url=test_depends.urls.rules("/get"),
            headers=class_db_auth_header,
        )

        assert response.status_code == 200

        try:
            task_id_schema = TaskIDValidationSchema.model_validate_json(response.content)
        except ValidationError as exc:
            pytest.fail(f'Ednpoint "/get" response validation error, exc: {exc}')

        for _ in range(3):
            response = await class_httpx_client.get(
                url=test_depends.urls.task_response(f"/get/{task_id_schema.task_id}"),
                headers=class_db_auth_header,
            )

            assert response.status_code == 200

            try:
                task_response_schema = APITaskResponseSchema.model_validate_json(response.content)
            except ValidationError as exc:
                pytest.fail(f'Ednpoint "/get" response validation error, exc: {exc}')

            if not task_response_schema.ready:
                await asyncio.sleep(2)
                continue

            assert task_response_schema.successful

            try:
                ModerationRulesSchema.model_validate(task_response_schema.content["rules"])
            except ValidationError as exc:
                pytest.fail(f'Ednpoint "/get" response validation error, exc: {exc}')
