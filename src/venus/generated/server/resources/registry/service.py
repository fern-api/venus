import abc
import inspect
import typing

import fastapi

from ...core.abstract_fern_service import AbstractFernService
from ...core.route_args import get_route_args
from .types.check_registry_permission_request import CheckRegistryPermissionRequest
from .types.generate_registry_tokens_request import GenerateRegistryTokensRequest
from .types.registry_tokens import RegistryTokens


class AbstractRegistryService(AbstractFernService):
    """
    AbstractRegistryService is an abstract class containing the methods that your
    RegistryService implementation should implement.

    Each method is associated with an API route, which will be registered
    with FastAPI when you register your implementation using Fern's register()
    function.
    """

    @abc.abstractmethod
    def generate_registry_tokens(self, *, request: GenerateRegistryTokensRequest) -> RegistryTokens:
        ...

    @abc.abstractmethod
    def has_registry_permission(self, *, request: CheckRegistryPermissionRequest) -> bool:
        ...

    """
    Below are internal methods used by Fern to register your implementation.
    You can ignore them.
    """

    @classmethod
    def _init_fern(cls, router: fastapi.APIRouter) -> None:
        cls.__init_generate_registry_tokens(router=router)
        cls.__init_has_registry_permission(router=router)

    @classmethod
    def __init_generate_registry_tokens(cls, router: fastapi.APIRouter) -> None:
        endpoint_function = inspect.signature(cls.generate_registry_tokens)
        new_parameters: typing.List[inspect.Parameter] = []
        for index, (parameter_name, parameter) in enumerate(endpoint_function.parameters.items()):
            if index == 0:
                new_parameters.append(parameter.replace(default=fastapi.Depends(cls)))
            elif parameter_name == "request":
                new_parameters.append(parameter.replace(default=fastapi.Body(...)))
            else:
                new_parameters.append(parameter)
        setattr(cls.generate_registry_tokens, "__signature__", endpoint_function.replace(parameters=new_parameters))

        cls.generate_registry_tokens = router.post(  # type: ignore
            path="/registry/generate-tokens",
            response_model=RegistryTokens,
            **get_route_args(cls.generate_registry_tokens),
        )(cls.generate_registry_tokens)

    @classmethod
    def __init_has_registry_permission(cls, router: fastapi.APIRouter) -> None:
        endpoint_function = inspect.signature(cls.has_registry_permission)
        new_parameters: typing.List[inspect.Parameter] = []
        for index, (parameter_name, parameter) in enumerate(endpoint_function.parameters.items()):
            if index == 0:
                new_parameters.append(parameter.replace(default=fastapi.Depends(cls)))
            elif parameter_name == "request":
                new_parameters.append(parameter.replace(default=fastapi.Body(...)))
            else:
                new_parameters.append(parameter)
        setattr(cls.has_registry_permission, "__signature__", endpoint_function.replace(parameters=new_parameters))

        cls.has_registry_permission = router.post(  # type: ignore
            path="/registry/check-permissions", response_model=bool, **get_route_args(cls.has_registry_permission)
        )(cls.has_registry_permission)