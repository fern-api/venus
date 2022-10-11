import typing

import pydantic
import typing_extensions

from ...commons.types.organization_id import OrganizationId


class OrganizationsPage(pydantic.BaseModel):
    organizations: typing.List[OrganizationId]
    next_page: typing.Optional[int] = pydantic.Field(alias="nextPage")

    @pydantic.validator("organizations")
    def _validate_organizations(cls, organizations: typing.List[OrganizationId]) -> typing.List[OrganizationId]:
        for validator in OrganizationsPage.Validators._organizations:
            organizations = validator(organizations)
        return organizations

    @pydantic.validator("next_page")
    def _validate_next_page(cls, next_page: typing.Optional[int]) -> typing.Optional[int]:
        for validator in OrganizationsPage.Validators._next_page:
            next_page = validator(next_page)
        return next_page

    class Validators:
        _organizations: typing.ClassVar[
            typing.List[typing.Callable[[typing.List[OrganizationId]], typing.List[OrganizationId]]]
        ] = []
        _next_page: typing.ClassVar[typing.List[typing.Callable[[typing.Optional[int]], typing.Optional[int]]]] = []

        @typing.overload
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["organizations"]
        ) -> typing.Callable[
            [typing.Callable[[typing.List[OrganizationId]], typing.List[OrganizationId]]],
            typing.Callable[[typing.List[OrganizationId]], typing.List[OrganizationId]],
        ]:
            ...

        @typing.overload
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["next_page"]
        ) -> typing.Callable[
            [typing.Callable[[typing.Optional[int]], typing.Optional[int]]],
            typing.Callable[[typing.Optional[int]], typing.Optional[int]],
        ]:
            ...

        @classmethod
        def field(cls, field_name: str) -> typing.Any:
            def decorator(validator: typing.Any) -> typing.Any:
                if field_name == "organizations":
                    cls._organizations.append(validator)
                elif field_name == "next_page":
                    cls._next_page.append(validator)
                else:
                    raise RuntimeError("Field does not exist on OrganizationsPage: " + field_name)

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
