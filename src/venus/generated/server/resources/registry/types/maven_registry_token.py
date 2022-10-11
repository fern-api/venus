import typing

import pydantic
import typing_extensions


class MavenRegistryToken(pydantic.BaseModel):
    username: str
    password: str

    @pydantic.validator("username")
    def _validate_username(cls, username: str) -> str:
        for validator in MavenRegistryToken.Validators._username:
            username = validator(username)
        return username

    @pydantic.validator("password")
    def _validate_password(cls, password: str) -> str:
        for validator in MavenRegistryToken.Validators._password:
            password = validator(password)
        return password

    class Validators:
        _username: typing.ClassVar[typing.List[typing.Callable[[str], str]]] = []
        _password: typing.ClassVar[typing.List[typing.Callable[[str], str]]] = []

        @typing.overload
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["username"]
        ) -> typing.Callable[[typing.Callable[[str], str]], typing.Callable[[str], str]]:
            ...

        @typing.overload
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["password"]
        ) -> typing.Callable[[typing.Callable[[str], str]], typing.Callable[[str], str]]:
            ...

        @classmethod
        def field(cls, field_name: str) -> typing.Any:
            def decorator(validator: typing.Any) -> typing.Any:
                if field_name == "username":
                    cls._username.append(validator)
                elif field_name == "password":
                    cls._password.append(validator)
                else:
                    raise RuntimeError("Field does not exist on MavenRegistryToken: " + field_name)

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
