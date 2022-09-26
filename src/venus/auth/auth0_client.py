from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

from venus.config import VenusConfig


class VenusAuth0Client:
    def __init__(self, auth0: Auth0):
        self.auth0 = auth0

    def create_organization(self, org_id: str) -> str:
        create_auth0_organization_response = (
            self.auth0.organizations.create_organization({"name": org_id})
        )
        print(
            "Created organization in auth0. Received response: ",
            create_auth0_organization_response,
        )
        return create_auth0_organization_response["id"]


class Auth0Client:
    def __init__(self, config: VenusConfig):
        self.config = config
        self.mgmt_api_token: str = None
        self.expiry: str = None

    def get(self) -> VenusAuth0Client:
        self._ensure_token_valid()
        auth0 = Auth0(
            self.config.auth0_mgmt_audience,
            self.mgmt_api_token,
        )
        return VenusAuth0Client(auth0)

    def _ensure_token_valid(self):
        if self.mgmt_api_token is None:
            print(self.config.auth0_domain_name)
            get_token = GetToken(self.config.auth0_domain_name)
            token = get_token.client_credentials(
                client_id=self.config.auth0_client_id,
                client_secret=self.config.auth0_client_secret,
                audience=self.config.auth0_mgmt_audience,
            )
            self.mgmt_api_token = token["access_token"]
