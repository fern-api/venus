from __future__ import annotations

import typing

import pydantic
import typing_extensions

from .maven_registry_token import MavenRegistryToken
from .npm_registry_token import NpmRegistryToken

T_Result = typing.TypeVar("T_Result")


class _Factory:
    def npm(self, value: NpmRegistryToken) -> RegistryToken:
        return RegistryToken(__root__=_RegistryToken.Npm(**dict(value), type="npm"))

    def maven(self, value: MavenRegistryToken) -> RegistryToken:
        return RegistryToken(__root__=_RegistryToken.Maven(**dict(value), type="maven"))


class RegistryToken(pydantic.BaseModel):
    factory: typing.ClassVar[_Factory] = _Factory()

    def get(self) -> typing.Union[_RegistryToken.Npm, _RegistryToken.Maven]:
        return self.__root__

    def visit(
        self, npm: typing.Callable[[NpmRegistryToken], T_Result], maven: typing.Callable[[MavenRegistryToken], T_Result]
    ) -> T_Result:
        if self.__root__.type == "npm":
            return npm(self.__root__)
        if self.__root__.type == "maven":
            return maven(self.__root__)

    __root__: typing_extensions.Annotated[
        typing.Union[_RegistryToken.Npm, _RegistryToken.Maven], pydantic.Field(discriminator="type")
    ]


class _RegistryToken:
    class Npm(NpmRegistryToken):
        type: typing_extensions.Literal["npm"]

    class Maven(MavenRegistryToken):
        type: typing_extensions.Literal["maven"]


RegistryToken.update_forward_refs()
