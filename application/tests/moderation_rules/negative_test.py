from __future__ import annotations

from typing import TYPE_CHECKING

from core.taskiq.task_messages import TaskResponseMessages
from tests.testing_core.schemas.task_message import TaskMessageSchema
from tests.testing_core.unit_helpers.validation.task_response import task_response_validate

if TYPE_CHECKING:
    from httpx import AsyncClient
    from tests.testing_core.schemas.rules import RulesSchema


class NegativeModerationRulesTest:
    async def test_create_rules_with_wrong_json_data(
        self,
        class_db_auth_header: dict,
        class_httpx_client: AsyncClient,
        rules_model: RulesSchema,
        url_rules,
    ):
        response = await class_httpx_client.post(
            url=url_rules.create,
            headers=class_db_auth_header,
            json={"rules1": rules_model.rules},
        )

        assert response.status_code == 422

    async def test_get_rules_after_delete(
        self,
        class_db_auth_header: dict,
        class_httpx_client: AsyncClient,
        url_rules,
    ):
        response = await class_httpx_client.post(
            url=url_rules.get,
            headers=class_db_auth_header,
        )

        assert response.status_code == 200

        content = await task_response_validate(
            class_db_auth_header,
            class_httpx_client,
            response_content=response.content,
            validation_model=TaskMessageSchema,
            unsuccessful_ok=True,
        )

        assert content.message == TaskResponseMessages.RULES_NOT_FOUND

    async def test_delete_rules_after_delete(
        self,
        class_db_auth_header: dict,
        class_httpx_client: AsyncClient,
        url_rules,
    ):
        response = await class_httpx_client.delete(
            url=url_rules.delete,
            headers=class_db_auth_header,
        )

        assert response.status_code == 200

        content = await task_response_validate(
            class_db_auth_header,
            class_httpx_client,
            response_content=response.content,
            validation_model=TaskMessageSchema,
            unsuccessful_ok=True,
        )

        assert content.message == TaskResponseMessages.RULES_NOT_FOUND
