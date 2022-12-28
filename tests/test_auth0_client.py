import os

from uuid import uuid4

import pytest

from venus.auth.auth0_client import Auth0Client
from venus.config import VenusConfig


@pytest.mark.skip(reason="requires hitting auth0")
def test_auth0_create_org() -> None:
    auth0_client = Auth0Client(
        config=VenusConfig(
            auth0_client_id="8lyAgexpGrHZLhN2i1FNPSicjupACR1r",
            auth0_client_secret=os.getenv("VENUS_DEV_AUTH0_CLIENT_SECRET"),
            auth0_domain_name="fern-dev.us.auth0.com",
            auth0_mgmt_audience="https://fern-dev.us.auth0.com/api/v2/",
            auth0_venus_audience="venus-dev",
            nursery_origin="fake",
        )
    )
    venus_auth0_client = auth0_client.get()
    generated_org_name = "test_" + str(uuid4())
    venus_auth0_client.create_organization(org_id=generated_org_name)
    print("Created org " + generated_org_name)


@pytest.mark.skip(reason="requires hitting auth0")
def test_auth0_refresh_token() -> None:
    auth0_client = Auth0Client(
        config=VenusConfig(
            auth0_client_id="8lyAgexpGrHZLhN2i1FNPSicjupACR1r",
            auth0_client_secret=os.getenv("VENUS_DEV_AUTH0_CLIENT_SECRET"),
            auth0_domain_name="fern-dev.us.auth0.com",
            auth0_mgmt_audience="https://fern-dev.us.auth0.com/api/v2/",
            auth0_venus_audience="venus-dev",
            nursery_origin="fake",
        )
    )
    auth0_client._ensure_token_valid()


@pytest.mark.skip(reason="requires hitting auth0")
def test_auth0_get_user() -> None:
    token = "YOUR_TOKEN_HERE"
    auth0_client = Auth0Client(
        config=VenusConfig(
            auth0_client_id="8lyAgexpGrHZLhN2i1FNPSicjupACR1r",
            auth0_client_secret=os.getenv("VENUS_DEV_AUTH0_CLIENT_SECRET"),
            auth0_domain_name="fern-dev.us.auth0.com",
            auth0_mgmt_audience="https://fern-dev.us.auth0.com/api/v2/",
            auth0_venus_audience="venus-dev",
            nursery_origin="fake",
        )
    )
    user_id = auth0_client.get_user_id_from_token(token)
    print(f"user_id: {user_id}")
    user = auth0_client.get().get_user(user_id=user_id)
    print(user.json())
