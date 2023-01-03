from typing import List
from urllib.parse import urljoin

import requests

from fern.nursery import CreateTokenRequest
from fern.nursery import RevokeTokenRequest
from fern.nursery import TokenMetadata
from pydantic import parse_obj_as

from ..._core import Response
from ..._core.response import FailedResponse
from ..._core.response import SuccessResponse
from ..owner import OwnerId
from .types import CreateTokenResponse
from .types import GetTokenMetadataRequest


class TokenService:
    def __init__(self, origin: str):
        self.origin = origin if origin.endswith("/") else origin + "/"

    def create(
        self, *, body: CreateTokenRequest
    ) -> Response[CreateTokenResponse, None]:
        response = requests.post(
            url=urljoin(self.origin, "tokens/create"),
            headers={
                "Content-Type": "application/json",
            },
            data=body.json(by_alias=True),
        )
        if response.status_code >= 200 and response.status_code < 300:
            return SuccessResponse(
                ok=True, body=CreateTokenResponse.parse_raw(response.text)
            )
        else:
            return FailedResponse(ok=False, error=None)

    def get_token_metadata(
        self, *, body: GetTokenMetadataRequest
    ) -> Response[TokenMetadata, None]:
        response = requests.post(
            url=urljoin(self.origin, "tokens/metadata"),
            headers={
                "Content-Type": "application/json",
            },
            data=body.json(by_alias=True),
        )
        if response.status_code >= 200 and response.status_code < 300:
            return SuccessResponse(
                ok=True, body=TokenMetadata.parse_raw(response.text)
            )
        else:
            return FailedResponse(ok=False, error=None)

    def get_tokens_for_owner(
        self, *, owner_id: OwnerId
    ) -> Response[List[TokenMetadata], None]:
        response = requests.get(
            url=urljoin(self.origin, f"tokens/owner/{owner_id}"),
        )
        if response.status_code >= 200 and response.status_code < 300:
            return SuccessResponse(
                ok=True, body=parse_obj_as(List[TokenMetadata], response.text)
            )
        else:
            return FailedResponse(ok=False, error=None)

    def revoke_token(
        self, *, body: RevokeTokenRequest
    ) -> Response[None, None]:
        response = requests.post(
            url=urljoin(self.origin, "tokens/revoke"),
        )
        if response.status_code >= 200 and response.status_code < 300:
            return SuccessResponse(ok=True, body=None)
        else:
            return FailedResponse(ok=False, error=None)
