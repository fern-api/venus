import typing

import pydantic

from .owner_id import OwnerId


class Owner(pydantic.BaseModel):
    owner_id: OwnerId = pydantic.Field(alias="ownerId")
    data: typing.Any

    class Config:
        allow_population_by_field_name = True
