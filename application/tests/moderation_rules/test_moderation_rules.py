from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from core.taskiq.task_messages import TaskResponseMessages
from tests.testing_core.additional_checks.task_response import class_task_response_check
from tests.testing_core.schemas.validation.rules import RulesValidationSchema
from tests.testing_core.schemas.validation.task_message import TaskMessageValidationSchema

if TYPE_CHECKING:
    from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="class")
class TestModerationRules:
    async def test_create_rules(
        self,
        class_db_auth_header: dict,
        class_httpx_client: AsyncClient,
        moderation_rules: dict,
        url_rules,
    ):
        response = await class_httpx_client.post(
            url=url_rules.create,
            headers=class_db_auth_header,
            json=moderation_rules,
        )

        assert response.status_code == 200

        await class_task_response_check(
            class_db_auth_header,
            class_httpx_client,
            response_content=response.content,
            validation_model=None,
        )

    async def test_get_rules(
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

        await class_task_response_check(
            class_db_auth_header,
            class_httpx_client,
            response_content=response.content,
            validation_model=RulesValidationSchema,
        )

    async def test_delete_rules_1(
        self,
        class_db_auth_header: dict,
        class_httpx_client: AsyncClient,
        url_rules,
    ):
        response = await class_httpx_client.delete(
            url=url_rules.delete,
            headers=class_db_auth_header,
        )

        await class_task_response_check(
            class_db_auth_header,
            class_httpx_client,
            response_content=response.content,
            validation_model=None,
        )

    async def test_delete_rules_2(
        self,
        class_db_auth_header: dict,
        class_httpx_client: AsyncClient,
        url_rules,
    ):
        response = await class_httpx_client.delete(
            url=url_rules.delete,
            headers=class_db_auth_header,
        )

        content = await class_task_response_check(
            class_db_auth_header,
            class_httpx_client,
            response_content=response.content,
            validation_model=TaskMessageValidationSchema,
            unsuccessful_ok=True,
        )

        assert content.message == TaskResponseMessages.RULES_NOT_FOUND

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

        content = await class_task_response_check(
            class_db_auth_header,
            class_httpx_client,
            response_content=response.content,
            validation_model=TaskMessageValidationSchema,
            unsuccessful_ok=True,
        )

        assert content.message == TaskResponseMessages.RULES_NOT_FOUND
