from pydantic import BaseModel, ConfigDict


class APITaskResponseSchema(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    ready: bool
    successful: bool | None
    content: dict | None
