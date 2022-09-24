import os

from dataclasses import dataclass


AUTH0_DOMAIN_NAME_ENV_VAR = "AUTH0_DOMAIN_NAME"
NURSERY_URL_ENV_VAR = "NURSERY_URL"


@dataclass
class VenusConfig:
    auth0_domain_name: str
    nursery_url: str


def getConfig() -> VenusConfig:
    return VenusConfig(
        auth0_domain_name=_getEnvVarOrThrow(AUTH0_DOMAIN_NAME_ENV_VAR),
        nursery_url=_getEnvVarOrThrow(NURSERY_URL_ENV_VAR),
    )


def _getEnvVarOrThrow(env_var: str) -> str:
    val = os.getenv(env_var)
    if val is None:
        raise Exception(f"Environment variable {env_var} was undefined!")
    return val
