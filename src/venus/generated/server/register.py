# This file was auto-generated by Fern from our API Definition.

# flake8: noqa
# fmt: off
# isort: skip_file

import glob
import importlib
import os
import types

import fastapi
import starlette

from .core.abstract_fern_service import AbstractFernService
from .core.exceptions import (
    FernHTTPException,
    default_exception_handler,
    fern_http_exception_handler,
    http_exception_handler,
)
from .resources.organization.service import AbstractOrganizationService
from .resources.registry.service import AbstractRegistryService


def register(
    app: fastapi.FastAPI, *, organization: AbstractOrganizationService, registry: AbstractRegistryService
) -> None:
    app.include_router(__register_service(organization))
    app.include_router(__register_service(registry))

    app.add_exception_handler(FernHTTPException, fern_http_exception_handler)
    app.add_exception_handler(starlette.exceptions.HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, default_exception_handler)


def __register_service(service: AbstractFernService) -> fastapi.APIRouter:
    router = fastapi.APIRouter()
    type(service)._init_fern(router)
    return router


def register_validators(module: types.ModuleType) -> None:
    validators_directory: str = os.path.dirname(module.__file__)  # type: ignore
    for path in glob.glob("**/*.py", root_dir=validators_directory, recursive=True):
        absolute_path = os.path.join(validators_directory, path)
        if os.path.isfile(absolute_path):
            module_path = ".".join([module.__name__] + path.removesuffix(".py").split("/"))
            importlib.import_module(module_path)
