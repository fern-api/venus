from uuid import uuid4
from venus.auth.auth0_client import Auth0Client
from venus.config import VenusConfig

def test_auth0_client() -> None:
    auth0_client = Auth0Client(config=VenusConfig(
        auth0_client_id="8lyAgexpGrHZLhN2i1FNPSicjupACR1r",
        auth0_client_secret="kKvItycZHH6T9mYTZIiI_XleyissokeLlnQMugd16a2FNNws0emsMD_YqnQFsrOE",
        auth0_domain_name="fern-dev.us.auth0.com",
        auth0_mgmt_audience="https://fern-dev.us.auth0.com/api/v2/",
        cloudmap_name="fake"
    ))
    venus_auth0_client = auth0_client.get()
    generated_org_name = "test_" + str(uuid4());
    venus_auth0_client.create_organization(generated_org_name)
    print("Created org " + generated_org_name)