import pydantic

from .token_id import TokenId


class CreateTokenResponse(pydantic.BaseModel):
    token: str
    token_id: TokenId = pydantic.Field(alias="tokenId")

    class Config:
        allow_population_by_field_name = True
