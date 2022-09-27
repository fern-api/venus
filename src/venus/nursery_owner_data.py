import pydantic


class NurseryOrgData(pydantic.BaseModel):
    auth0_id: str

    class Config:
        allow_population_by_field_name = True
