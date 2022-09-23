import pydantic


class NpmRegistryToken(pydantic.BaseModel):
    token: str
