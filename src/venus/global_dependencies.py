import functools

from venus.auth.auth0_client import Auth0Client
from venus.config import VenusConfig


config = VenusConfig.create()


@functools.lru_cache()
def get_auth0() -> Auth0Client:
    return Auth0Client(config=config)
