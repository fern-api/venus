import typing

import pydantic

from ..commons.organization_id import OrganizationId


class OrganizationsPage(pydantic.BaseModel):
    organizations: typing.List[OrganizationId]
    next_page: typing.Optional[int] = pydantic.Field(alias="nextPage")

    class Config:
        allow_population_by_field_name = True
