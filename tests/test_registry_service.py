import json

from uuid import uuid4

from fastapi.testclient import TestClient

from venus.global_dependencies import get_nursery_client
from venus.main import app

from .http_utils import assert_valid_status_code


client = TestClient(app)
nursery_client = get_nursery_client()


def test_generate_and_use_token(nursery_docker) -> None:  # type: ignore
    # create org
    org_id = str(uuid4())
    create_org_response = client.post(
        "/organizations/create",
        json={"organizationId": org_id, "artifactReadRequiresToken": True},
    )
    assert_valid_status_code(create_org_response.status_code, "create_org")

    # generate token
    gen_token_response = client.post(
        "/registry/generate-tokens", json={"organizationId": org_id}
    )
    print(gen_token_response.text)
    assert_valid_status_code(gen_token_response.status_code, "generate_token")

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

    my_org = client.post(
        "/organizations/myself",
        headers={"Authorization": f"Bearer {npm_token}"},
    )
    assert my_org.status_code == 200
