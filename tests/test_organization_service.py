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


def test_create_org() -> None:
    client = TestClient(app)
    response = client.post(
        "/organizations/create", json={"organizationId": "fern"}
    )
    assert response.status_code == 200
