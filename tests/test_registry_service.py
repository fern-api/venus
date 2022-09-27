import json

from uuid import uuid4

import pytest
import requests

from fastapi.testclient import TestClient

from venus.global_dependencies import config
from venus.global_dependencies import get_nursery_client
from venus.main import app
from venus.nursery.resources.owner.types.create_owner_request import (
    CreateOwnerRequest,
)


client = TestClient(app)
nursery_client = get_nursery_client()


def is_responsive(url: str):  # type: ignore
    try:
        response = requests.get(url)
        print(response)
        if response.status_code == 204:
            return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def nursery_docker(docker_ip, docker_services):  # type: ignore
    print(config.nursery_origin + "/health")
    docker_services.wait_until_responsive(
        timeout=30.0,
        pause=1,
        check=lambda: is_responsive(config.nursery_origin + "/health"),
    )


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
