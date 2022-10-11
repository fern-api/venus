import typing

import pydantic
import typing_extensions


class NpmRegistryToken(pydantic.BaseModel):
    token: str

    @pydantic.validator("token")
    def _validate_token(cls, token: str) -> str:
        for validator in NpmRegistryToken.Validators._token:
            token = validator(token)
        return token

    class Validators:
        _token: typing.ClassVar[typing.List[typing.Callable[[str], str]]] = []

        @typing.overload  # type: ignore
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["token"]
        ) -> typing.Callable[[typing.Callable[[str], str]], typing.Callable[[str], str]]:
            ...

        @classmethod
        def field(cls, field_name: str) -> typing.Any:
            def decorator(validator: typing.Any) -> typing.Any:
                if field_name == "token":
                    cls._token.append(validator)
                else:
                    raise RuntimeError("Field does not exist on NpmRegistryToken: " + field_name)

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
