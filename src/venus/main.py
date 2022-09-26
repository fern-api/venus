import uvicorn

from fastapi import FastAPI

from venus import global_dependencies
from venus import organization_service
from venus import registry_service


app = FastAPI()
app.include_router(organization_service.router)
app.include_router(registry_service.router)


@app.get("/health")
def health() -> None:
    pass


def start() -> None:
    """Launched with `poetry run start` at root level"""

    print("Auth0 Client id is ", global_dependencies.config.auth0_client_id)

    uvicorn.run(
        "venus.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )


if __name__ == "__main__":
    start()
