from core.models import db_attach
from core.models.moderation_rule import ModerationRule
from core.schemas.moderation_rules import ModerationRulesSchema
from core.schemas.task_response import TaskResponseSchema
from core.taskiq.broker import broker
from core.taskiq.task_runtime_logger import task_runtime_logger
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


async def turn_to_numbered(rules_dict: dict[str : dict[str, str]]) -> dict[str : dict[str, str]]:
    rule_dict = rules_dict["rules"]
    numbered_rule_dict = {}

    for index, items in enumerate(rule_dict.items()):
        rule = items[0]
        action = items[1]

        numbered_rule_dict.update({index: {rule: action}})

    return {"rules_numbered": numbered_rule_dict}


@broker.task
async def set_moderation_rules_db_task(user_id: int, rules_schema: ModerationRulesSchema) -> TaskResponseSchema:
    response = TaskResponseSchema(successful=False, content=None)

    try:
        async with db_attach.session_factory() as session:
            query = select(ModerationRule).where(ModerationRule.user_id == user_id)
            sqla_result = await session.execute(query)
            moderation_rule = sqla_result.scalar_one_or_none()

            rule_dict = rules_schema.model_dump()
            numbered_rule_dict = await turn_to_numbered(rule_dict)

            if moderation_rule:
                moderation_rule.rules = rule_dict
                moderation_rule.rules_numbered = numbered_rule_dict
            else:
                moderation_rule = ModerationRule(
                    user_id=user_id,
                    rules=rule_dict,
                    rules_numbered=numbered_rule_dict,
                )

                session.add(moderation_rule)

            await session.commit()

            response.successful = True
    except SQLAlchemyError:
        task_runtime_logger.logger.error("SQLAlchemy exception", exc_info=True)
    except ValidationError:
        task_runtime_logger.logger.error("Rules dict dump error", exc_info=True)
    except Exception:
        task_runtime_logger.logger.error("Unexpected exception", exc_info=True)

    return response
