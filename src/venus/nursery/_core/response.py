from __future__ import annotations

from dataclasses import dataclass
from typing import Generic
from typing import TypeVar
from typing import Union

from typing_extensions import Literal


OkBody = TypeVar("OkBody")
ErrorBody = TypeVar("ErrorBody")


@dataclass
class SuccessResponse(Generic[OkBody]):
    ok: Literal[True]
    body: OkBody


@dataclass
class FailedResponse(Generic[ErrorBody]):
    ok: Literal[False]
    error: ErrorBody


Response = Union[SuccessResponse[OkBody], FailedResponse[ErrorBody]]
