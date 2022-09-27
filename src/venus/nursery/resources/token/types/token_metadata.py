import typing

import pydantic

from ...owner import OwnerId
from .token_id import TokenId


class TokenMetadata(pydantic.BaseModel):
    token_id: TokenId = pydantic.Field(alias="tokenId")
    owner_id: OwnerId = pydantic.Field(alias="ownerId")
    description: typing.Optional[str]

    class Config:
        allow_population_by_field_name = True
