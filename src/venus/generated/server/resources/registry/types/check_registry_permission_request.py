import typing

import pydantic
import typing_extensions

from ...commons.types.organization_id import OrganizationId
from .registry_token import RegistryToken


class CheckRegistryPermissionRequest(pydantic.BaseModel):
    organization_id: OrganizationId = pydantic.Field(alias="organizationId")
    token: typing.Optional[RegistryToken]

    @pydantic.validator("organization_id")
    def _validate_organization_id(cls, organization_id: OrganizationId) -> OrganizationId:
        for validator in CheckRegistryPermissionRequest.Validators._organization_id:
            organization_id = validator(organization_id)
        return organization_id

    @pydantic.validator("token")
    def _validate_token(cls, token: typing.Optional[RegistryToken]) -> typing.Optional[RegistryToken]:
        for validator in CheckRegistryPermissionRequest.Validators._token:
            token = validator(token)
        return token

    class Validators:
        _organization_id: typing.ClassVar[typing.List[typing.Callable[[OrganizationId], OrganizationId]]] = []
        _token: typing.ClassVar[
            typing.List[typing.Callable[[typing.Optional[RegistryToken]], typing.Optional[RegistryToken]]]
        ] = []

        @typing.overload
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["organization_id"]
        ) -> typing.Callable[
            [typing.Callable[[OrganizationId], OrganizationId]], typing.Callable[[OrganizationId], OrganizationId]
        ]:
            ...

        @typing.overload
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["token"]
        ) -> typing.Callable[
            [typing.Callable[[typing.Optional[RegistryToken]], typing.Optional[RegistryToken]]],
            typing.Callable[[typing.Optional[RegistryToken]], typing.Optional[RegistryToken]],
        ]:
            ...

        @classmethod
        def field(cls, field_name: str) -> typing.Any:
            def decorator(validator: typing.Any) -> typing.Any:
                if field_name == "organization_id":
                    cls._organization_id.append(validator)
                elif field_name == "token":
                    cls._token.append(validator)
                else:
                    raise RuntimeError("Field does not exist on CheckRegistryPermissionRequest: " + field_name)

                return validator

            return decorator

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        allow_population_by_field_name = True
