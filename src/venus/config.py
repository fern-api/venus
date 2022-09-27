from __future__ import annotations

import os

from dataclasses import dataclass


AUTH0_DOMAIN_NAME_ENV_VAR = "AUTH0_DOMAIN_NAME"
AUTH0_CLIENT_ID_ENV_VAR = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV_VAR = "AUTH0_CLIENT_SECRET"
AUTH0_MGMT_AUDIENCE_ENV_VAR = "AUTH0_MGMT_AUDIENCE"
NURSERY_ORIGIN_ENV_VAR = "NURSERY_ORIGIN"


@dataclass
class VenusConfig:
    auth0_domain_name: str
    auth0_client_id: str
    auth0_client_secret: str
    auth0_mgmt_audience: str
    nursery_origin: str

    @staticmethod
    def __get_env_var_or_throw(env_var: str) -> str:
        val = os.getenv(env_var)
        if val is None:
            raise Exception(f"Environment variable {env_var} was undefined!")
        return val

    @classmethod
    def create(cls) -> VenusConfig:
        return cls(
            auth0_domain_name=VenusConfig.__get_env_var_or_throw(
                AUTH0_DOMAIN_NAME_ENV_VAR
            ),
            auth0_client_id=VenusConfig.__get_env_var_or_throw(
                AUTH0_CLIENT_ID_ENV_VAR
            ),
            auth0_client_secret=VenusConfig.__get_env_var_or_throw(
                AUTH0_CLIENT_SECRET_ENV_VAR
            ),
            auth0_mgmt_audience=VenusConfig.__get_env_var_or_throw(
                AUTH0_MGMT_AUDIENCE_ENV_VAR
            ),
            nursery_origin=VenusConfig.__get_env_var_or_throw(
                NURSERY_ORIGIN_ENV_VAR
            ),
        )
