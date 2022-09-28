import typing

import pydantic

from ..commons.organization_id import OrganizationId
from .registry_token import RegistryToken


class CheckRegistryPermissionRequest(pydantic.BaseModel):
    organization_id: OrganizationId = pydantic.Field(alias="organizationId")
    token: typing.Optional[RegistryToken]

    class Config:
        allow_population_by_field_name = True
