import typing

import pydantic

from ...owner import OwnerId


class CreateTokenRequest(pydantic.BaseModel):
    owner_id: OwnerId = pydantic.Field(alias="ownerId")
    description: typing.Optional[str]

    class Config:
        allow_population_by_field_name = True
