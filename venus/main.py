from fastapi import FastAPI
import uvicorn

app = FastAPI()


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