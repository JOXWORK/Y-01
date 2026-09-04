from core.schemas.task_response import TaskResponseSchema
from core.taskiq.result_backend import result_backend

from api.schemas.v1.api_task_response import APITaskResponseSchema


async def get_result(task_id: str) -> APITaskResponseSchema:
    api_response = APITaskResponseSchema(
        ready=False,
        successful=None,
        content=None,
    )

    is_result_ready = await result_backend.is_result_ready(task_id)
    if is_result_ready:
        task_result = await result_backend.get_result(task_id)
        task_response = TaskResponseSchema(**task_result.return_value)

        task_successful = task_response.successful

        api_response.ready = True
        api_response.successful = task_successful
        api_response.content = task_response.content

        if not task_successful:
            api_response.content = {"message": "Internal task error"}

    return api_response
