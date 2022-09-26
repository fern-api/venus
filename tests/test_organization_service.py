from fastapi.testclient import TestClient

from venus.main import app


client = TestClient(app)


def test_create_org() -> None:
    pass
    # response = client.post(
    #     "/organizations/create", json={"organizationId": "fern"}
    # )
    # assert response.status_code == 200
