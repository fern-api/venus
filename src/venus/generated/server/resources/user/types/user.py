import typing

import pydantic
import typing_extensions


class User(pydantic.BaseModel):
    username: str

    @pydantic.validator("username")
    def _validate_username(cls, username: str) -> str:
        for validator in User.Validators._username:
            username = validator(username)
        return username

    class Validators:
        _username: typing.ClassVar[typing.List[typing.Callable[[str], str]]] = []

        @typing.overload  # type: ignore
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["username"]
        ) -> typing.Callable[[typing.Callable[[str], str]], typing.Callable[[str], str]]:
            ...

        @classmethod
        def field(cls, field_name: str) -> typing.Any:
            def decorator(validator: typing.Any) -> typing.Any:
                if field_name == "username":
                    cls._username.append(validator)
                else:
                    raise RuntimeError("Field does not exist on User: " + field_name)

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
