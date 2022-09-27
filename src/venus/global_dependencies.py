import functools

from venus.auth.auth0_client import Auth0Client
from venus.config import VenusConfig
from venus.nursery.client import NurseryApiClient


config = VenusConfig.create()


@functools.lru_cache()
def get_auth0() -> Auth0Client:
    return Auth0Client(config=config)


@functools.lru_cache()
def get_nursery_client() -> NurseryApiClient:
    return NurseryApiClient(
        origin=f"http://nursery.{config.cloudmap_name}:8080"
    )
