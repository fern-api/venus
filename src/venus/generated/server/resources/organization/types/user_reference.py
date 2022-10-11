from __future__ import annotations

import typing

import pydantic
import typing_extensions

from ...commons.types.user_id import UserId

T_Result = typing.TypeVar("T_Result")


class _Factory:
    def user_id(self, value: UserId) -> UserReference:
        return UserReference(__root__=_UserReference.UserId(type="userId", user_id=value))

    def email_address(self, value: str) -> UserReference:
        return UserReference(__root__=_UserReference.EmailAddress(type="emailAddress", email_address=value))


class UserReference(pydantic.BaseModel):
    factory: typing.ClassVar[_Factory] = _Factory()

    def get_as_union(self) -> typing.Union[_UserReference.UserId, _UserReference.EmailAddress]:
        return self.__root__

    def visit(
        self, user_id: typing.Callable[[UserId], T_Result], email_address: typing.Callable[[str], T_Result]
    ) -> T_Result:
        if self.__root__.type == "userId":
            return user_id(self.__root__.user_id)
        if self.__root__.type == "emailAddress":
            return email_address(self.__root__.email_address)

    __root__: typing_extensions.Annotated[
        typing.Union[_UserReference.UserId, _UserReference.EmailAddress], pydantic.Field(discriminator="type")
    ]

    @pydantic.root_validator
    def _validate(cls, values: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        value = typing.cast(typing.Union[_UserReference.UserId, _UserReference.EmailAddress], values.get("__root__"))
        for validator in UserReference.Validators._validators:
            value = validator(value)
        return {**values, "__root__": value}

    class Validators:
        _validators: typing.ClassVar[
            typing.List[
                typing.Callable[
                    [typing.Union[_UserReference.UserId, _UserReference.EmailAddress]],
                    typing.Union[_UserReference.UserId, _UserReference.EmailAddress],
                ]
            ]
        ] = []

        @classmethod
        def validate(
            cls,
            validator: typing.Callable[
                [typing.Union[_UserReference.UserId, _UserReference.EmailAddress]],
                typing.Union[_UserReference.UserId, _UserReference.EmailAddress],
            ],
        ) -> None:
            cls._validators.append(validator)

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True


class _UserReference:
    class UserId(pydantic.BaseModel):
        type: typing_extensions.Literal["userId"]
        user_id: UserId = pydantic.Field(alias="userId")

        class Config:
            frozen = True
            allow_population_by_field_name = True

    class EmailAddress(pydantic.BaseModel):
        type: typing_extensions.Literal["emailAddress"]
        email_address: str = pydantic.Field(alias="emailAddress")

        class Config:
            frozen = True
            allow_population_by_field_name = True


UserReference.update_forward_refs()