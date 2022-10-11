import typing

import pydantic
import typing_extensions

from .maven_registry_token import MavenRegistryToken
from .npm_registry_token import NpmRegistryToken


class RegistryTokens(pydantic.BaseModel):
    npm: NpmRegistryToken
    maven: MavenRegistryToken

    @pydantic.validator("npm")
    def _validate_npm(cls, npm: NpmRegistryToken) -> NpmRegistryToken:
        for validator in RegistryTokens.Validators._npm:
            npm = validator(npm)
        return npm

    @pydantic.validator("maven")
    def _validate_maven(cls, maven: MavenRegistryToken) -> MavenRegistryToken:
        for validator in RegistryTokens.Validators._maven:
            maven = validator(maven)
        return maven

    class Validators:
        _npm: typing.ClassVar[typing.List[typing.Callable[[NpmRegistryToken], NpmRegistryToken]]] = []
        _maven: typing.ClassVar[typing.List[typing.Callable[[MavenRegistryToken], MavenRegistryToken]]] = []

        @typing.overload
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["npm"]
        ) -> typing.Callable[
            [typing.Callable[[NpmRegistryToken], NpmRegistryToken]],
            typing.Callable[[NpmRegistryToken], NpmRegistryToken],
        ]:
            ...

        @typing.overload
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["maven"]
        ) -> typing.Callable[
            [typing.Callable[[MavenRegistryToken], MavenRegistryToken]],
            typing.Callable[[MavenRegistryToken], MavenRegistryToken],
        ]:
            ...

        @classmethod
        def field(cls, field_name: str) -> typing.Any:
            def decorator(validator: typing.Any) -> typing.Any:
                if field_name == "npm":
                    cls._npm.append(validator)
                elif field_name == "maven":
                    cls._maven.append(validator)
                else:
                    raise RuntimeError("Field does not exist on RegistryTokens: " + field_name)

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
