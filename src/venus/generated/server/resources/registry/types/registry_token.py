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

    def get_as_union(self) -> typing.Union[_RegistryToken.Npm, _RegistryToken.Maven]:
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

    @pydantic.root_validator
    def _validate(cls, values: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        value = typing.cast(typing.Union[_RegistryToken.Npm, _RegistryToken.Maven], values.get("__root__"))
        for validator in RegistryToken.Validators._validators:
            value = validator(value)
        return {**values, "__root__": value}

    class Validators:
        _validators: typing.ClassVar[
            typing.List[
                typing.Callable[
                    [typing.Union[_RegistryToken.Npm, _RegistryToken.Maven]],
                    typing.Union[_RegistryToken.Npm, _RegistryToken.Maven],
                ]
            ]
        ] = []

        @classmethod
        def validate(
            cls,
            validator: typing.Callable[
                [typing.Union[_RegistryToken.Npm, _RegistryToken.Maven]],
                typing.Union[_RegistryToken.Npm, _RegistryToken.Maven],
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


class _RegistryToken:
    class Npm(NpmRegistryToken):
        type: typing_extensions.Literal["npm"]

        class Config:
            frozen = True

    class Maven(MavenRegistryToken):
        type: typing_extensions.Literal["maven"]

        class Config:
            frozen = True


RegistryToken.update_forward_refs()