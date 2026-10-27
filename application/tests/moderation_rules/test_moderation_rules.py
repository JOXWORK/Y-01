import pytest
from httpx import AsyncClient
from tests.testing_core.schemas.task_id_validation import TaskIDValidationSchema
from tests.testing_core.test_depends import test_depends


@pytest.mark.asyncio(loop_scope="class")
class TestModerationRules:
    async def test_create_rules(self, class_db_auth_header: dict, class_httpx_client: AsyncClient, moderation_rules: dict):
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

        TaskIDValidationSchema.model_validate_json(response.content)
