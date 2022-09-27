from urllib.parse import parse_qsl

from fastapi.testclient import TestClient

from venus.main import app


client = TestClient(app)


def test_generate_registry_tokens() -> None:
    # response = client.post(
    #     "/registry/generate-tokens", json={"organizationId": "fern"}
    # )
    # assert response.status_code == 200
    parse_qsl


def test_has_registry_permission() -> None:
    # response = client.post(
    #     "/registry/check-permissions",
    #     json={
    #         "organizationId": "fern",
    #         "token": {"type": "npm", "token": "fake"},
    #     },
    # )
    # assert response.status_code == 200
    pass
