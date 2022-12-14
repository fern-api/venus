import traceback
import typing

from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timedelta
from typing import Optional

import jwt

from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0

from venus.config import VenusConfig
from venus.generated.server.resources.commons import UnauthorizedError
from venus.generated.server.resources.organization import (
    OrganizationAlreadyExistsError,
)
from venus.generated.server.resources.user.types.user import User


class AbstractVenusAuth0Client(ABC):
    @abstractmethod
    def create_organization(self, *, org_id: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, *, user_id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_orgs_for_user(self, *, user_id: str) -> typing.Set[str]:
        raise NotImplementedError

    @abstractmethod
    def add_user_to_org(self, *, user_id: str, org_id: str) -> None:
        raise NotImplementedError


class VenusAuth0Client(AbstractVenusAuth0Client):
    def __init__(self, auth0: Auth0):
        self.auth0 = auth0

    def create_organization(self, *, org_id: str) -> str:
        try:
            create_auth0_organization_response = (
                self.auth0.organizations.create_organization({"name": org_id})
            )
        except Auth0Error as e:
            if e.status_code == 409:
                print(f"An organization with name {org_id} already exists")
                raise OrganizationAlreadyExistsError()
        print(
            "Created organization in auth0. Received response: ",
            create_auth0_organization_response,
        )
        return create_auth0_organization_response["id"]

    def get_user(self, *, user_id: str) -> User:
        get_user_response = self.auth0.users.get(user_id)
        return User(
            username=get_user_response["nickname"],
            user_id=get_user_response["user_id"],
            email=get_user_response["email"],
        )

    def get_orgs_for_user(self, *, user_id: str) -> typing.Set[str]:
        # TODO(dsinghvi): Fix, page through all orgs
        list_organizatins_response = self.auth0.users.list_organizations(
            user_id
        )
        organization_ids = set()
        for organization in list_organizatins_response["organizations"]:
            organization_ids.add(organization["id"])
        return organization_ids

    def add_user_to_org(self, *, user_id: str, org_id: str) -> None:
        self.auth0.organizations.create_organization_members(
            org_id, {"members": [user_id]}
        )


class AbstractAuth0Client(ABC):
    @abstractmethod
    def get(self) -> AbstractVenusAuth0Client:
        raise NotImplementedError()

    @abstractmethod
    def get_user_id_from_token(self, token: str) -> str:
        raise NotImplementedError()


class Auth0Client(AbstractAuth0Client):
    def __init__(self, config: VenusConfig):
        self.config = config
        self.mgmt_api_token: Optional[str] = None
        self.expiry_time: Optional[datetime] = None
        jwks_url = (
            f"https://{self.config.auth0_domain_name}/.well-known/jwks.json"
        )
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def get(self) -> VenusAuth0Client:
        self._ensure_token_valid()
        auth0 = Auth0(
            self.config.auth0_domain_name,
            self.mgmt_api_token,
        )
        return VenusAuth0Client(auth0)

    def get_user_id_from_token(self, token: str) -> str:
        try:
            expected_issuer = (
                self.config.auth0_domain_name
                if self.config.auth0_domain_name.startswith("http")
                else f"https://{self.config.auth0_domain_name}/"
            )
            print(expected_issuer)
            signing_key = self.jwks_client.get_signing_key_from_jwt(token).key
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                issuer=expected_issuer,
                audience=self.config.auth0_venus_audience,
            )
            return payload["sub"]
        except Exception:
            print(traceback.format_exc())
            raise UnauthorizedError()

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
