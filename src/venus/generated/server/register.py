import fastapi

from .core.abstract_fern_service import AbstractFernService
from .core.exceptions import FernHTTPException
from .resources.organization.service import AbstractOrganizationService
from .resources.registry.service import AbstractRegistryService


def register(
    app: fastapi.FastAPI, *, organization: AbstractOrganizationService, registry: AbstractRegistryService
) -> None:
    app.include_router(__register_service(organization))
    app.include_router(__register_service(registry))

    @app.exception_handler(FernHTTPException)
    def _exception_handler(request: fastapi.requests.Request, exc: FernHTTPException) -> fastapi.responses.JSONResponse:
        return exc.to_json_response()


def __register_service(service: AbstractFernService) -> fastapi.APIRouter:
    router = fastapi.APIRouter()
    type(service)._init_fern(router)
    return router
