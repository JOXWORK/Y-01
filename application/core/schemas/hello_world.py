from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, field_validator, model_validator
from pydantic_core import PydanticCustomError

if TYPE_CHECKING:
    from typing_extensions import Self


class HelloWorldSchema(BaseModel):
    Hello: str
    World: str

    foo: int

    @model_validator(mode="after")
    def internal_validator(self) -> Self:
        if self.Hello != "Hello":
            raise PydanticCustomError(
                "HelloError",
                '{hello_arg} is not equal "Hello"',
                {"hello_args": self.Hello},
            )
        if self.World != "World":
            raise PydanticCustomError(
                "WorldError",
                '{world_arg} is not equal "World"',
                {"world_arg": self.World},
            )

        return self

    @field_validator("foo", mode="before")
    @classmethod
    def foo_field_validator(cls, data: int):
        if data != 12:
            if int(data) != 12:
                raise ValueError(f"{data} is not number 12")

        return data


def main():
    Hello = "Hello"
    World = "World"
    foo = 12

    schema = HelloWorldSchema(  # noqa: F841
        Hello=Hello,
        World=World,
        foo=foo,
    )


if __name__ == "__main__":
    main()
