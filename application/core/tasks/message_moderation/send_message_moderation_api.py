from core.config import settings
from core.models.db_attach import db_attach
from core.models.moderation_rule import ModerationRule
from core.openai_client.client import openai_client
from core.promts.message_moderation import system_promt
from core.schemas.moderation_response import ModerationResponseSchema
from core.taskiq.broker import broker
from core.taskiq.task_runtime_logger import task_runtime_logger
from openai import OpenAIError
from pydantic import ValidationError
from sqlalchemy import select


async def generate_user_promt(message: str, rules: dict):
    return f"""
    <rules>
    {rules}
    </rules>

    <message>
    {message}
    </message>
    """


async def get_moderation_rules(user_id: int):
    async with db_attach.session_factory() as session:
        query = select(ModerationRule).where(ModerationRule.user_id == user_id)
        sqla_result = await session.execute(query)

        moderation_rule = sqla_result.scalar_one_or_none()

        if moderation_rule is None:
            return None

        return moderation_rule.rules


@broker.task
async def send_message_moderation_api_task(message: str, user_id: int) -> ModerationResponseSchema | None:
    moderation_result = None
    content = None

    try:
        rules = await get_moderation_rules(user_id)
        USER_PROMT = await generate_user_promt(
            message=message,
            rules=rules,
        )

        response = await openai_client.chat.completions.create(
            model=settings.cloud_ru_api.model,
            messages=[
                {
                    "role": "developer",
                    "content": system_promt.PROMT,
                },
                {
                    "role": "user",
                    "content": USER_PROMT,
                },
            ],
        )

        content = response.choices[0].message.content
        moderation_result = ModerationResponseSchema.model_validate_json(content)
    except OpenAIError:
        task_runtime_logger.logger.error(
            f"Openai module exception, LLM response: {content}",
            exc_info=True,
        )
    except ValidationError:
        task_runtime_logger.logger.error(
            f"LLM response validation exception, LLM response: {content}",
            exc_info=True,
        )
    except Exception:
        task_runtime_logger.logger.error(
            f"Unexpected exception, LLM response: {content}",
            exc_info=True,
        )

    return moderation_result
