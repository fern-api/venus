# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import pydantic
import typing_extensions

from ...commons.types.organization_id import OrganizationId


class Organization(pydantic.BaseModel):
    organization_id: OrganizationId = pydantic.Field(alias="organizationId")
    artifact_read_requires_token: bool = pydantic.Field(alias="artifactReadRequiresToken")

    class Partial(typing_extensions.TypedDict):
        organization_id: typing_extensions.NotRequired[OrganizationId]
        artifact_read_requires_token: typing_extensions.NotRequired[bool]

    class Validators:
        """
        Use this class to add validators to the Pydantic model.

            @Organization.Validators.root
            def validate(values: Organization.Partial) -> Organization.Partial:
                ...

            @Organization.Validators.field("organization_id")
            def validate_organization_id(organization_id: OrganizationId, values: Organization.Partial) -> OrganizationId:
                ...

            @Organization.Validators.field("artifact_read_requires_token")
            def validate_artifact_read_requires_token(artifact_read_requires_token: bool, values: Organization.Partial) -> bool:
                ...
        """

        _validators: typing.ClassVar[typing.List[typing.Callable[[Organization.Partial], Organization.Partial]]] = []
        _organization_id_validators: typing.ClassVar[typing.List[Organization.Validators.OrganizationIdValidator]] = []
        _artifact_read_requires_token_validators: typing.ClassVar[
            typing.List[Organization.Validators.ArtifactReadRequiresTokenValidator]
        ] = []

        @classmethod
        def root(
            cls, validator: typing.Callable[[Organization.Partial], Organization.Partial]
        ) -> typing.Callable[[Organization.Partial], Organization.Partial]:
            cls._validators.append(validator)
            return validator

        @typing.overload
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["organization_id"]
        ) -> typing.Callable[
            [Organization.Validators.OrganizationIdValidator], Organization.Validators.OrganizationIdValidator
        ]:
            ...

        @typing.overload
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["artifact_read_requires_token"]
        ) -> typing.Callable[
            [Organization.Validators.ArtifactReadRequiresTokenValidator],
            Organization.Validators.ArtifactReadRequiresTokenValidator,
        ]:
            ...

        @classmethod
        def field(cls, field_name: str) -> typing.Any:
            def decorator(validator: typing.Any) -> typing.Any:
                if field_name == "organization_id":
                    cls._organization_id_validators.append(validator)
                if field_name == "artifact_read_requires_token":
                    cls._artifact_read_requires_token_validators.append(validator)
                return validator

            return decorator

        class OrganizationIdValidator(typing_extensions.Protocol):
            def __call__(self, __v: OrganizationId, __values: Organization.Partial) -> OrganizationId:
                ...

        class ArtifactReadRequiresTokenValidator(typing_extensions.Protocol):
            def __call__(self, __v: bool, __values: Organization.Partial) -> bool:
                ...

    @pydantic.root_validator
    def _validate(cls, values: Organization.Partial) -> Organization.Partial:
        for validator in Organization.Validators._validators:
            values = validator(values)
        return values

    @pydantic.validator("organization_id")
    def _validate_organization_id(cls, v: OrganizationId, values: Organization.Partial) -> OrganizationId:
        for validator in Organization.Validators._organization_id_validators:
            v = validator(v, values)
        return v

    @pydantic.validator("artifact_read_requires_token")
    def _validate_artifact_read_requires_token(cls, v: bool, values: Organization.Partial) -> bool:
        for validator in Organization.Validators._artifact_read_requires_token_validators:
            v = validator(v, values)
        return v

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        allow_population_by_field_name = True
