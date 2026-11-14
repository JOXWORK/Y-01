import pytest_asyncio
from core.models.user import User
from core.tasks.moderation_rules.delete_moderation_rules import DeleteModerationRules


@pytest_asyncio.fixture(scope="function", loop_scope="class")
async def class_db_delete_rules(class_db_user: User):
    yield

    delete_task_response = await DeleteModerationRules(class_db_user.id)
    assert delete_task_response.successful
