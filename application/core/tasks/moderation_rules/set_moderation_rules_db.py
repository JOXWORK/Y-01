from core.models import db_attach
from core.models.moderation_rule import ModerationRule
from core.schemas.moderation_rules import ModerationRulesSchema
from core.schemas.task_response import TaskResponseSchema
from core.taskiq.broker import broker
from core.taskiq.task_runtime_logger import task_runtime_logger
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


async def add_id_to_rule(rules_dict: dict[str : dict[str, str]]) -> dict[str : dict[str, str]]:
    rule_dict = rules_dict["rules"]
    id_rule_dict = {}

    for index, items in enumerate(rule_dict.items()):
        rule = items[0]
        action = items[1]

        id_rule = f"{index}: {rule}"
        id_rule_dict[id_rule] = action

    return {"rules": id_rule_dict}


@broker.task
async def set_moderation_rules_db_task(user_id: int, rules_schema: ModerationRulesSchema) -> TaskResponseSchema:
    response = TaskResponseSchema(successful=False, content=None)

    try:
        async with db_attach.session_factory() as session:
            query = select(ModerationRule).where(ModerationRule.user_id == user_id)
            sqla_result = await session.execute(query)
            moderation_rule = sqla_result.scalar_one_or_none()

            rules_dict = rules_schema.model_dump()
            id_rules_dict = await add_id_to_rule(rules_dict)

            if moderation_rule:
                moderation_rule.rules = id_rules_dict
            else:
                moderation_rule = ModerationRule(
                    user_id=user_id,
                    rules=id_rules_dict,
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
