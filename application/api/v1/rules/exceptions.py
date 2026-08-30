from core.http.error_details._rules import RulesErrorDetails
from fastapi import HTTPException, status


def http_wrong_task_result():
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail=RulesErrorDetails.WRONG_TASK_RESULT,
    )
