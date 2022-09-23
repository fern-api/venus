import pydantic


class MavenRegistryToken(pydantic.BaseModel):
    username: str
    password: str
