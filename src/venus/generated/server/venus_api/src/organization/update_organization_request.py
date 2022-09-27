
import pydantic


class UpdateOrganizationRequest(pydantic.BaseModel):
    artifact_read_requires_token: bool = pydantic.Field(
        alias="artifactReadRequiresToken"
    )

    class Config:
        allow_population_by_field_name = True
