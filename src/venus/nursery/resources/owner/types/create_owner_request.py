import typing

import pydantic


class CreateOwnerRequest(pydantic.BaseModel):
    owner_id: str = pydantic.Field(alias="ownerId")
    data: typing.Any

    class Config:
        allow_population_by_field_name = True
