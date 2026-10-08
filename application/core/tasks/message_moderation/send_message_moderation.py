from core.config import settings
from core.llm_response_journal.journal import LLMResponseJournalWriteError, llm_response_journal
from core.openai_client.client import openai_client
from core.promts.message_moderation import system_promt
from core.schemas.moderation_response import ModerationLLMResponseSchema
from core.schemas.task_response import TaskResponseSchema
from core.task_depends.get_moderation_rules import getModerationRules
from core.taskiq.broker import broker
from core.taskiq.except_messages import TaskExceptionMessages
from core.taskiq.task_logger import get_task_logger
from core.taskiq.task_messages import TaskResponseMessages, create_message
from openai import OpenAIError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from taskiq import Context, TaskiqDepends

logger = get_task_logger()


def generate_user_promt(message: str, rules: dict):
    return f"""
    <rules>
    {rules}
    </rules>

    <message>
    {message}
    </message>
    """


@broker.task
async def SendMessageModeration(
    message: str,
    user_id: int,
    context: Context = TaskiqDepends(),
) -> TaskResponseSchema:
    response = TaskResponseSchema(successful=False, content=None)

    try:
        moderation_rules = await getModerationRules(user_id)

        if moderation_rules:
            rules = moderation_rules["rules_numbered"]

            PROMT = generate_user_promt(
                message=message,
                rules=rules,
            )

            llm_response = await openai_client.chat.completions.create(
                model=settings.cloud_ru_api.model,
                messages=[
                    {
                        "role": "developer",
                        "content": system_promt.PROMT,
                    },
                    {
                        "role": "user",
                        "content": PROMT,
                    },
                ],
            )

            llm_content = llm_response.choices[0].message.content.strip()
            await llm_response_journal.write(
                key_name=context.message.task_id,
                content=llm_content,
            )

            response.content = ModerationLLMResponseSchema.model_validate_json(
                llm_content,
            ).model_dump()
            response.successful = True
        else:
            response.content = create_message(TaskResponseMessages.RULES_NOT_FOUND)
    except OpenAIError:
        logger.error("Openai module exception", exc_info=True)
    except ValidationError:
        logger.error("LLM response validation exception", exc_info=True)
    except LLMResponseJournalWriteError:
        logger.error("LLM response journal write error", exc_info=True)
    except SQLAlchemyError:
        logger.enum_error(TaskExceptionMessages.SQLALCHEMY_EXCEPTION)
    except Exception:
        logger.enum_error(TaskExceptionMessages.UNEXPECTED_EXCEPTION)

    return response
