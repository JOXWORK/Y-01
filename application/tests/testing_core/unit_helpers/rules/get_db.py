from core.tasks.moderation_rules.get_moderation_rules import GetModerationRules

from tests.testing_core.schemas.rules import RulesValidationSchema


async def get_db_rules(user_id: int) -> RulesValidationSchema | None:
    get_task_response = await GetModerationRules(user_id)

    if get_task_response.successful:
        content = get_task_response.content
        rules = RulesValidationSchema(
            rules=content["rules"],
            rules_numbered=content["rules_numbered"],
        )

        return rules

    return None
