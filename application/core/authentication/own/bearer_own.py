from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import status

if TYPE_CHECKING:
    from fastapi import Response
    from fastapi_users.openapi import OpenAPIResponseType

from fastapi.responses import JSONResponse
from fastapi_users.authentication import BearerTransport
from pydantic import BaseModel


class BearerResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class BearerTransportOwn(BearerTransport):
    def __init__(self, tokenUrl):
        super().__init__(tokenUrl)

    async def get_login_response(self, access_token: str, refresh_token: str) -> Response:
        bearer_response = await self._token_pair_response(access_token=access_token, refresh_token=refresh_token)
        return JSONResponse(bearer_response.model_dump())

    async def get_reissue_response(self, access_token: str, refresh_token: str) -> Response:
        bearer_response = await self._token_pair_response(access_token=access_token, refresh_token=refresh_token)
        return JSONResponse(bearer_response.model_dump())

    async def _token_pair_response(self, access_token: str, refresh_token: str, token_type: str = "bearer") -> BearerResponse:
        return BearerResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
        )

    @staticmethod
    def get_openapi_login_responses_success() -> OpenAPIResponseType:
        return {
            status.HTTP_200_OK: {
                "model": BearerResponse,
                "content": {
                    "application/json": {
                        "example": {
                            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1"
                            "c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2Z"
                            "DMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS"
                            "11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ."
                            "M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
                            "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1"
                            "c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2Z"
                            "DMtY2U2NDJjYmE1NjAzIiwic2Vzc2lvbl9pZCI6Mj"
                            "U2LCJhdWQiOiJmYXN0YXBpLXVzZXJzOmF1dGgiLCJ"
                            "jcmVhdGVkX2F0IjoxNzgzNjczNDIxLCJyZXZva2Vk"
                            "X2F0IjpudWxsLCJ1c2VkX2F0IjpudWxsfQ.17j0tJ"
                            "jleDIWoOj7KWR3K1xW-loMhLK0vMWCGgyBI48",
                            "token_type": "bearer",
                        }
                    }
                },
            },
        }
