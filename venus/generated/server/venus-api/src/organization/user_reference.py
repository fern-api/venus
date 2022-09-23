from __future__ import annotations

import typing

import pydantic
import typing_extensions

from ..commons.user_id import UserId

T_Result = typing.TypeVar("T_Result")


class _Factory:
    def user_id(self, value: UserId) -> UserReference:
        return UserReference(__root__=_UserReference.UserId(type="userId", user_id=value))

    def email_address(self, value: str) -> UserReference:
        return UserReference(__root__=_UserReference.EmailAddress(type="emailAddress", email_address=value))


class UserReference(pydantic.BaseModel):
    factory: typing.ClassVar[_Factory] = _Factory()

    def get(self) -> typing.Union[_UserReference.UserId, _UserReference.EmailAddress]:
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


class _UserReference:
    class UserId(pydantic.BaseModel):
        type: typing_extensions.Literal["userId"]
        user_id: UserId = pydantic.Field(alias="userId")

        class Config:
            allow_population_by_field_name = True

    class EmailAddress(pydantic.BaseModel):
        type: typing_extensions.Literal["emailAddress"]
        email_address: str = pydantic.Field(alias="emailAddress")

        class Config:
            allow_population_by_field_name = True


UserReference.update_forward_refs()
