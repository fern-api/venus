from uuid import uuid4

from fastapi.testclient import TestClient

from venus.global_dependencies import get_auth0
from venus.global_dependencies import get_nursery_client
from venus.main import app

from .mock_auth0_client import MockAuth0Client


client = TestClient(app)


app.dependency_overrides[get_auth0] = lambda: MockAuth0Client()


def test_create_and_update_org(nursery_docker):  # type: ignore
    # create_org
    org_id = str(uuid4())
    create_org_response = client.post(
        "/organizations/create", json={"organizationId": org_id}
    )
    assert create_org_response.status_code == 204
    # get org from nursery
    get_owner_response = get_nursery_client().owner.get(owner_id=org_id)
    if get_owner_response.ok:
        print("get_owner_response", get_owner_response.body)
        assert (
            get_owner_response.body.data["artifactReadRequiresToken"] is False
        )
    else:
        raise Exception(
            "Failed to get owner from nursery", get_owner_response.error
        )

    # update_org
    update_org_response = client.post(
        f"/organizations/{org_id}/update",
        json={"artifactReadRequiresToken": True},
    )
    assert update_org_response.status_code == 204
    # get org from nursery
    get_owner_response = get_nursery_client().owner.get(owner_id=org_id)
    if get_owner_response.ok:
        print("get_owner_response", get_owner_response.body)
        assert (
            get_owner_response.body.data["artifactReadRequiresToken"] is True
        )
    else:
        raise Exception(
            "Failed to get owner from nursery", get_owner_response.error
        )
