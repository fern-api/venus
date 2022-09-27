import pydantic


class GetTokenMetadataRequest(pydantic.BaseModel):
    token: str

    class Config:
        allow_population_by_field_name = True
