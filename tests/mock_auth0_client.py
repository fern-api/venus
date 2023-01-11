import typing

from typing import Dict
from uuid import uuid4

from venus.auth.auth0_client import AbstractAuth0Client
from venus.auth.auth0_client import AbstractVenusAuth0Client
from venus.generated.server.resources.user.types.user import User


class MockVenusAuth0Client(AbstractVenusAuth0Client):
    def __init__(self) -> None:
        self.org_id_to_auth0_id: Dict[str, str] = {}
        self.auth0_org_id_to_members: Dict[str, list[str]] = {}

    def create_organization(self, org_id: str) -> str:
        if org_id in self.org_id_to_auth0_id:
            raise Exception("Org already exists: ", org_id)
        auth0_id = str(uuid4())
        self.org_id_to_auth0_id[org_id] = auth0_id
        self.auth0_org_id_to_members[auth0_id] = []
        print(self.auth0_org_id_to_members)
        return auth0_id

    def get_user(self, *, user_id: str) -> User:
        return super().get_user(user_id=user_id)

    def get_orgs_for_user(self, *, user_id: str) -> typing.Set[str]:
        return super().get_orgs_for_user(user_id=user_id)

    def add_user_to_org(self, *, user_id: str, org_id: str) -> None:
        if org_id in self.auth0_org_id_to_members:
            self.auth0_org_id_to_members[org_id].append(user_id)
        print(f"Org id {org_id} not in created orgs")


class MockAuth0Client(AbstractAuth0Client):
    def get(self) -> MockVenusAuth0Client:
        return MockVenusAuth0Client()

    def get_user_id_from_token(self, token: str) -> str:
        return "github|12303"
