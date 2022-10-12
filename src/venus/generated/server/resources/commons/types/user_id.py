# This file was auto-generated by Fern from our API Definition.

# flake8: noqa
# fmt: off
# isort: skip_file

from __future__ import annotations

import typing

import pydantic


class UserId(pydantic.BaseModel):
    __root__: str

    def get_as_str(self) -> str:
        return self.__root__

    @staticmethod
    def from_str(value: str) -> UserId:
        return UserId(__root__=value)

    class Validators:
        """
        Use this class to add validators to the Pydantic model.

            @UserId.Validators.validate
            def validate(value: str) -> str:
                ...
        """

        _validators: typing.ClassVar[typing.List[typing.Callable[[str], str]]] = []

        @classmethod
        def validate(cls, validator: typing.Callable[[str], str]) -> None:
            cls._validators.append(validator)

    @pydantic.root_validator
    def _validate(cls, values: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        value = typing.cast(str, values.get("__root__"))
        for validator in UserId.Validators._validators:
            value = validator(value)
        return {**values, "__root__": value}

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
