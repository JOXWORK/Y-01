from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from negative_test import NegativeModerationRulesTest
from tests.testing_core.schemas.rules import RulesSchema
from tests.testing_core.unit_helpers.rules.get_db import get_db_rules
from tests.testing_core.unit_helpers.validation.task_response import task_response_validate

if TYPE_CHECKING:
    from core.models.user import User
    from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="class")
class TestModerationRules(NegativeModerationRulesTest):
    async def test_create_rules(
        self,
        class_db_auth_header: dict,
        class_httpx_client: AsyncClient,
        rules_model: RulesSchema,
        url_rules,
        class_db_user: User,
        class_db_delete_rules,
    ):
        response = await class_httpx_client.post(
            url=url_rules.create,
            headers=class_db_auth_header,
            json={"rules": rules_model.rules},
        )

        assert response.status_code == 200

        await task_response_validate(
            class_db_auth_header,
            class_httpx_client,
            response_content=response.content,
            validation_model=None,
        )

        await get_db_rules(class_db_user.id)

    @pytest.mark.delete_rules(True)
    async def test_get_rules(
        self,
        class_db_auth_header: dict,
        class_httpx_client: AsyncClient,
        url_rules,
        class_db_rules: dict,
    ):
        response = await class_httpx_client.post(
            url=url_rules.get,
            headers=class_db_auth_header,
        )

        assert response.status_code == 200

        await task_response_validate(
            class_db_auth_header,
            class_httpx_client,
            response_content=response.content,
            validation_model=RulesSchema,
        )

        #! написать additional check на наличие в бд записи с правилами

    async def test_delete_rules(
        self,
        class_db_auth_header: dict,
        class_httpx_client: AsyncClient,
        url_rules,
        class_db_rules: dict,
    ):
        response = await class_httpx_client.delete(
            url=url_rules.delete,
            headers=class_db_auth_header,
        )

        assert response.status_code == 200

        await task_response_validate(
            class_db_auth_header,
            class_httpx_client,
            response_content=response.content,
            validation_model=None,
        )

        #! написать additional check на отсутствие в бд записи с правилами
