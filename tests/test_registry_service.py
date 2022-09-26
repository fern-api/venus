import os

from unittest import mock

import pytest

from fastapi.testclient import TestClient

from venus.main import app


@pytest.fixture(autouse=True)
def mock_settings_env_vars() -> None:
    with mock.patch.dict(
        os.environ,
        {
            "AUTH0_DOMAIN_NAME": "fake",
            "AUTH0_CLIENT_ID": "fake",
            "AUTH0_CLIENT_SECRET": "fake",
            "CLOUDMAP_NAME": "fake",
        },
    ):
        yield


def test_generate_registry_tokens() -> None:
    client = TestClient(app)
    response = client.post(
        "/registry/generate-tokens", json={"organizationId": "fern"}
    )
    assert response.status_code == 200


def test_has_registry_permission() -> None:
    client = TestClient(app)
    response = client.post(
        "/registry/check-permissions",
        json={
            "organizationId": "fern",
            "token": {"type": "npm", "token": "fake"},
        },
    )
    assert response.status_code == 200
