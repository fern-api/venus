from typing import Dict
from uuid import uuid4

from venus.auth.auth0_client import AbstractAuth0Client
from venus.auth.auth0_client import AbstractVenusAuth0Client


class MockVenusAuth0Client(AbstractVenusAuth0Client):
    def __init__(self) -> None:
        self.org_id_to_auth0_id: Dict[str, str] = {}

    def create_organization(self, org_id: str) -> str:
        if org_id in self.org_id_to_auth0_id:
            raise Exception("Org already exists: ", org_id)
        auth0_id = str(uuid4())
        self.org_id_to_auth0_id[org_id] = auth0_id
        return auth0_id


class MockAuth0Client(AbstractAuth0Client):
    def get(self) -> MockVenusAuth0Client:
        return MockVenusAuth0Client()
