from core.config import settings
from core.llm_response_journal.journal import LLMResponseJournalWriteError, llm_response_journal
from core.openai_client.client import openai_client
from core.promts.message_moderation import system_promt
from core.schemas.moderation_response import ModerationLLMResponseSchema
from core.schemas.task_response import TaskResponseSchema
from core.taskiq.broker import broker
from core.taskiq.task_messages import TaskResponseMessages, create_message
from core.taskiq.task_runtime_logger import task_runtime_logger
from core.tasks.micro_tasks.micro_get_moderation_rules import get_moderation_rules_micro_task
from openai import OpenAIError
from pydantic import ValidationError
from taskiq import Context, TaskiqDepends


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
async def send_message_moderation_api_task(
    message: str,
    user_id: int,
    context: Context = TaskiqDepends(),
) -> TaskResponseSchema:
    response = TaskResponseSchema(successful=False, content=None)

    try:
        rules_micro_task = await get_moderation_rules_micro_task.kiq(user_id=user_id)
        rules_micro_task_result = await rules_micro_task.wait_result()
        rules_micro_task_response = rules_micro_task_result.return_value

        if rules_micro_task_response.successful:
            rules = rules_micro_task_response.content["rules_numbered"]

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
        task_runtime_logger.logger.error(
            "Openai module exception",
            exc_info=True,
        )
    except ValidationError:
        task_runtime_logger.logger.error(
            "LLM response validation exception",
            exc_info=True,
        )
    except LLMResponseJournalWriteError:
        task_runtime_logger.logger.error(
            "LLM response journal write error",
            exc_info=True,
        )
    except Exception:
        task_runtime_logger.logger.error(
            "Unexpected exception",
            exc_info=True,
        )

    return response
