# This file was auto-generated by Fern from our API Definition.

# flake8: noqa
# fmt: off
# isort: skip_file

from __future__ import annotations

import typing

import pydantic
import typing_extensions

from ...commons.types.organization_id import OrganizationId


class GenerateRegistryTokensRequest(pydantic.BaseModel):
    organization_id: OrganizationId = pydantic.Field(alias="organizationId")

    class Validators:
        """
        Use this class to add validators to the Pydantic model.

            @GenerateRegistryTokensRequest.Validators.field("organization_id")
            def validate_organization_id(v: OrganizationId, values: GenerateRegistryTokensRequest.Partial) -> OrganizationId:
                ...
        """

        _organization_id_validators: typing.ClassVar[
            typing.List[GenerateRegistryTokensRequest.Validators.OrganizationIdValidator]
        ] = []

        @typing.overload  # type: ignore
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["organization_id"]
        ) -> typing.Callable[
            [GenerateRegistryTokensRequest.Validators.OrganizationIdValidator],
            GenerateRegistryTokensRequest.Validators.OrganizationIdValidator,
        ]:
            ...

        @classmethod
        def field(cls, field_name: str) -> typing.Any:
            def decorator(validator: typing.Any) -> typing.Any:
                if field_name == "organization_id":
                    cls._organization_id_validators.append(validator)
                return validator

            return decorator

        class OrganizationIdValidator(typing_extensions.Protocol):
            def __call__(self, v: OrganizationId, *, values: GenerateRegistryTokensRequest.Partial) -> OrganizationId:
                ...

    @pydantic.validator("organization_id")
    def _validate_organization_id(
        cls, v: OrganizationId, values: GenerateRegistryTokensRequest.Partial
    ) -> OrganizationId:
        for validator in GenerateRegistryTokensRequest.Validators._organization_id_validators:
            v = validator(v, values=values)
        return v

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Partial(typing_extensions.TypedDict):
        organization_id: typing_extensions.NotRequired[OrganizationId]

    class Config:
        frozen = True
        allow_population_by_field_name = True
