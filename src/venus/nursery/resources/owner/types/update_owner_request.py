import typing

import pydantic


class UpdateOwnerRequest(pydantic.BaseModel):
    data: typing.Any

    class Config:
        allow_population_by_field_name = True
