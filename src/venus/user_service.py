from fastapi import Depends
import venus.generated.server as fern

from venus.auth.auth0_client import AbstractAuth0Client, Auth0Client
from venus.generated.server.resources.user.types.organizations_page import (
    OrganizationsPage,
)
from venus.generated.server.resources.user.types.user import User
from venus.generated.server.security import ApiAuth
from venus.global_dependencies import get_auth0, get_nursery_client
from venus.nursery.client import NurseryApiClient


class UserService(fern.AbstractUserService):
    def __init__(
        self,
        auth0_client: Auth0Client = Depends(get_auth0),
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> None:
        self.nursery_client = nursery_client
        self.auth0_client = auth0_client

    def get_myself(self, *, auth: ApiAuth) -> User:
        user_id = self.auth0_client.get_user_id_from_token(auth.token)
        return self.auth0_client.get().get_user(user_id=user_id)

    def get_my_organizations(
        self, *, page_id: int, auth: ApiAuth
    ) -> OrganizationsPage:
        raise NotImplementedError()

    def belongs_to_organization(
        self, *, organization_id: str, auth: ApiAuth
    ) -> bool:
        raise NotImplementedError()
