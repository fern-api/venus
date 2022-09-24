import pydantic

from .maven_registry_token import MavenRegistryToken
from .npm_registry_token import NpmRegistryToken


class RegistryTokens(pydantic.BaseModel):
    npm: NpmRegistryToken
    maven: MavenRegistryToken
