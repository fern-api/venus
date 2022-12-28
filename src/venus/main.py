import uvicorn

from fastapi import FastAPI

from venus.generated.server.register import register
from venus.global_dependencies import get_auth0
from venus.global_dependencies import get_nursery_client
from venus.organization_service import OrganizationsService
from venus.registry_service import RegistryService
from venus.user_service import UserService


app = FastAPI()
register(
    app,
    organization=OrganizationsService(),
    registry=RegistryService(),
    user=UserService(
        nursery_client=get_nursery_client(), auth0_client=get_auth0()
    ),
)


@app.get("/health")
def health() -> None:
    pass


def start() -> None:
    """Launched with `poetry run start` at root level"""

    uvicorn.run(
        "venus.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )


if __name__ == "__main__":
    start()
