import uvicorn
from fastapi import FastAPI

from venus import organization_service, registry_service

app = FastAPI()
app.include_router(organization_service.router)
app.include_router(registry_service.router)


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
