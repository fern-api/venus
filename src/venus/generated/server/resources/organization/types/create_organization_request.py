import typing

import pydantic
import typing_extensions

from ...commons.types.organization_id import OrganizationId


class CreateOrganizationRequest(pydantic.BaseModel):
    organization_id: OrganizationId = pydantic.Field(alias="organizationId")
    artifact_read_requires_token: typing.Optional[bool] = pydantic.Field(alias="artifactReadRequiresToken")

    @pydantic.validator("organization_id")
    def _validate_organization_id(cls, organization_id: OrganizationId) -> OrganizationId:
        for validator in CreateOrganizationRequest.Validators._organization_id:
            organization_id = validator(organization_id)
        return organization_id

    @pydantic.validator("artifact_read_requires_token")
    def _validate_artifact_read_requires_token(
        cls, artifact_read_requires_token: typing.Optional[bool]
    ) -> typing.Optional[bool]:
        for validator in CreateOrganizationRequest.Validators._artifact_read_requires_token:
            artifact_read_requires_token = validator(artifact_read_requires_token)
        return artifact_read_requires_token

    class Validators:
        _organization_id: typing.ClassVar[typing.List[typing.Callable[[OrganizationId], OrganizationId]]] = []
        _artifact_read_requires_token: typing.ClassVar[
            typing.List[typing.Callable[[typing.Optional[bool]], typing.Optional[bool]]]
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
            cls, field_name: typing_extensions.Literal["artifact_read_requires_token"]
        ) -> typing.Callable[
            [typing.Callable[[typing.Optional[bool]], typing.Optional[bool]]],
            typing.Callable[[typing.Optional[bool]], typing.Optional[bool]],
        ]:
            ...

        @classmethod
        def field(cls, field_name: str) -> typing.Any:
            def decorator(validator: typing.Any) -> typing.Any:
                if field_name == "organization_id":
                    cls._organization_id.append(validator)
                elif field_name == "artifact_read_requires_token":
                    cls._artifact_read_requires_token.append(validator)
                else:
                    raise RuntimeError("Field does not exist on CreateOrganizationRequest: " + field_name)

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
