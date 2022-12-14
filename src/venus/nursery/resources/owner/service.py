from urllib.parse import urljoin

import requests

from ..._core import Response
from ..._core.response import FailedResponse
from ..._core.response import SuccessResponse
from .types import CreateOwnerRequest
from .types import Owner
from .types import OwnerId
from .types import UpdateOwnerRequest


class OwnerService:
    def __init__(self, origin: str):
        self.origin = origin if origin.endswith("/") else origin + "/"

    def create(self, *, body: CreateOwnerRequest) -> Response[None, None]:
        response = requests.post(
            url=urljoin(self.origin, "owner"),
            headers={
                "Content-Type": "application/json",
            },
            data=body.json(by_alias=True),
        )
        if response.status_code >= 200 and response.status_code < 300:
            return SuccessResponse(ok=True, body=None)
        else:
            return FailedResponse(ok=False, error=None)

    def get(self, *, owner_id: OwnerId) -> Response[Owner, None]:
        response = requests.get(url=urljoin(self.origin, f"owner/{owner_id}"))
        if response.status_code >= 200 and response.status_code < 300:
            return SuccessResponse(
                ok=True, body=Owner.parse_raw(response.text)
            )
        else:
            return FailedResponse(ok=False, error=None)

    def update(
        self, *, owner_id: OwnerId, body: UpdateOwnerRequest
    ) -> Response[Owner, None]:
        response = requests.put(
            url=urljoin(self.origin, f"owner/{owner_id}"),
            headers={
                "Content-Type": "application/json",
            },
            data=body.json(by_alias=True),
        )
        if response.status_code >= 200 and response.status_code < 300:
            return SuccessResponse(
                ok=True, body=Owner.parse_raw(response.text)
            )
        else:
            return FailedResponse(ok=False, error=None)
