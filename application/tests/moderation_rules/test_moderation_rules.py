from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from tests.testing_core.additional_checks.task_response import class_task_response_check
from tests.testing_core.schemas.validation.rules import RulesValidationSchema
from tests.testing_core.test_depends import test_depends

if TYPE_CHECKING:
    from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="class")
@pytest.mark.delay(3)
class TestModerationRules:
    async def test_create_rules(
        self,
        class_db_auth_header: dict,
        class_httpx_client: AsyncClient,
        moderation_rules: dict,
    ):
        response = await class_httpx_client.post(
            url=test_depends.urls.rules("/create"),
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
    ):
        response = await class_httpx_client.post(
            url=test_depends.urls.rules("/get"),
            headers=class_db_auth_header,
        )

        assert response.status_code == 200

        await class_task_response_check(
            class_db_auth_header,
            class_httpx_client,
            response_content=response.content,
            validation_model=RulesValidationSchema,
        )
