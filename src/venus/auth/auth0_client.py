from datetime import datetime
from datetime import timedelta
from typing import Optional

from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

from venus.config import VenusConfig

from abc import ABC, abstractmethod


class AbstractVenusAuth0Client(ABC):
    @abstractmethod
    def create_organization(self, org_id: str) -> str:
        raise NotImplementedError


class VenusAuth0Client(AbstractVenusAuth0Client):
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


class AbstractAuth0Client(ABC):
    @abstractmethod
    def get(self) -> AbstractVenusAuth0Client:
        raise NotImplementedError


class Auth0Client(AbstractAuth0Client):
    def __init__(self, config: VenusConfig):
        self.config = config
        self.mgmt_api_token: Optional[str] = None
        self.expiry_time: Optional[datetime] = None

    def get(self) -> VenusAuth0Client:
        self._ensure_token_valid()
        auth0 = Auth0(
            self.config.auth0_domain_name,
            self.mgmt_api_token,
        )
        return VenusAuth0Client(auth0)

    def _ensure_token_valid(self) -> None:
        if self.mgmt_api_token is None or self._is_expired():
            get_token = GetToken(self.config.auth0_domain_name)
            token = get_token.client_credentials(
                client_id=self.config.auth0_client_id,
                client_secret=self.config.auth0_client_secret,
                audience=self.config.auth0_mgmt_audience,
            )
            self.mgmt_api_token = token["access_token"]
            self.expiry_time = datetime.now() + timedelta(
                seconds=int(token["expires_in"]) - 1000
            )

    def _is_expired(self) -> bool:
        if self.expiry_time is not None:
            return datetime.now() > self.expiry_time
        return True
