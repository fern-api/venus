import typing

import pydantic
import typing_extensions


class UpdateOrganizationRequest(pydantic.BaseModel):
    artifact_read_requires_token: bool = pydantic.Field(alias="artifactReadRequiresToken")

    @pydantic.validator("artifact_read_requires_token")
    def _validate_artifact_read_requires_token(cls, artifact_read_requires_token: bool) -> bool:
        for validator in UpdateOrganizationRequest.Validators._artifact_read_requires_token:
            artifact_read_requires_token = validator(artifact_read_requires_token)
        return artifact_read_requires_token

    class Validators:
        _artifact_read_requires_token: typing.ClassVar[typing.List[typing.Callable[[bool], bool]]] = []

        @typing.overload  # type: ignore
        @classmethod
        def field(
            cls, field_name: typing_extensions.Literal["artifact_read_requires_token"]
        ) -> typing.Callable[[typing.Callable[[bool], bool]], typing.Callable[[bool], bool]]:
            ...

        @classmethod
        def field(cls, field_name: str) -> typing.Any:
            def decorator(validator: typing.Any) -> typing.Any:
                if field_name == "artifact_read_requires_token":
                    cls._artifact_read_requires_token.append(validator)
                else:
                    raise RuntimeError("Field does not exist on UpdateOrganizationRequest: " + field_name)

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
