import pytest
import pytest_asyncio
from core.models.user import User
from core.tasks.moderation_rules.delete_moderation_rules import DeleteModerationRules
from core.tasks.moderation_rules.set_moderation_rules import SetModerationRules

from tests.testing_core.schemas.rules import RulesSchema


@pytest.fixture(scope="class")
def moderation_rules():
    return {
        "rules": {
            "запрещена реклама": "ban",
            "запрещен спам": "mute",
            "запрещены оскорбления": "жick",
            "запрещена скрытая реклама": "ban",
            "запрещена реклама профиля": "ban",
            "запрещена реклама 18+ и не легальных ресурсов": "ban",
            "запрещена реклама игорных сервисов": "ban",
        }
    }


@pytest.fixture(scope="class")
def rules_model():
    return RulesSchema()


@pytest_asyncio.fixture(scope="function", loop_scope="class")
async def class_db_rules(
    request,
    class_db_user: User,
    rules_model: RulesSchema,
):
    delete_marker = request.node.get_closest_marker("delete_rules")
    user_id = class_db_user.id

    create_task_response = await SetModerationRules(
        user_id=user_id,
        rules=rules_model.rules,
        rules_numbered=rules_model.rules_numbered,
    )
    assert create_task_response.successful

    yield create_task_response.content

    if delete_marker:
        delete_task_response = await DeleteModerationRules(user_id=class_db_user.id)
        assert delete_task_response.successful
