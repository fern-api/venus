import json

from uuid import uuid4

from fastapi.testclient import TestClient

from venus.global_dependencies import get_nursery_client
from venus.main import app
from venus.nursery.resources.owner.types.create_owner_request import (
    CreateOwnerRequest,
)

from .docker_fixtures import nursery_docker


client = TestClient(app)
nursery_client = get_nursery_client()


def test_generate_and_use_token(nursery_docker) -> None:  # type: ignore
    # create org
    org_id = str(uuid4())
    nursery_client.owner.create(
        body=CreateOwnerRequest(owner_id=org_id, data=None)
    )
    # generate token
    gen_token_response = client.post(
        "/registry/generate-tokens", json={"organizationId": org_id}
    )
    print(gen_token_response.text)
    assert gen_token_response.status_code == 200
    # check token works
    npm_token = json.loads(gen_token_response.text)["npm"]["token"]
    print("npm token: ", npm_token)
    check_token_response = client.post(
        "/registry/check-permissions",
        json={
            "organizationId": org_id,
            "token": {
                "type": "npm",
                "token": npm_token,
            },
        },
    )
    assert check_token_response.status_code == 200
