import abc
import inspect
import typing

import fastapi

from ...core.abstract_fern_service import AbstractFernService
from ...core.route_args import get_route_args
from .types.create_organization_request import CreateOrganizationRequest
from .types.organization import Organization
from .types.update_organization_request import UpdateOrganizationRequest


class AbstractOrganizationService(AbstractFernService):
    """
    AbstractOrganizationService is an abstract class containing the methods that your
    OrganizationService implementation should implement.

    Each method is associated with an API route, which will be registered
    with FastAPI when you register your implementation using Fern's register()
    function.
    """

    @abc.abstractmethod
    def create(self, *, request: CreateOrganizationRequest) -> None:
        ...

    @abc.abstractmethod
    def update(self, *, request: UpdateOrganizationRequest, org_id: str) -> None:
        ...

    @abc.abstractmethod
    def get(self, *, org_id: str) -> Organization:
        ...

    """
    Below are internal methods used by Fern to register your implementation.
    You can ignore them.
    """

    @classmethod
    def _init_fern(cls, router: fastapi.APIRouter) -> None:
        cls.__init_create(router=router)
        cls.__init_update(router=router)
        cls.__init_get(router=router)

    @classmethod
    def __init_create(cls, router: fastapi.APIRouter) -> None:
        endpoint_function = inspect.signature(cls.create)
        new_parameters: typing.List[inspect.Parameter] = []
        for index, (parameter_name, parameter) in enumerate(endpoint_function.parameters.items()):
            if index == 0:
                new_parameters.append(parameter.replace(default=fastapi.Depends(cls)))
            elif parameter_name == "request":
                new_parameters.append(parameter.replace(default=fastapi.Body(...)))
            else:
                new_parameters.append(parameter)
        setattr(cls.create, "__signature__", endpoint_function.replace(parameters=new_parameters))

        cls.create = router.post(path="/organizations/create", **get_route_args(cls.create))(cls.create)  # type: ignore

    @classmethod
    def __init_update(cls, router: fastapi.APIRouter) -> None:
        endpoint_function = inspect.signature(cls.update)
        new_parameters: typing.List[inspect.Parameter] = []
        for index, (parameter_name, parameter) in enumerate(endpoint_function.parameters.items()):
            if index == 0:
                new_parameters.append(parameter.replace(default=fastapi.Depends(cls)))
            elif parameter_name == "request":
                new_parameters.append(parameter.replace(default=fastapi.Body(...)))
            elif parameter_name == "org_id":
                new_parameters.append(parameter.replace(default=fastapi.Path(...)))
            else:
                new_parameters.append(parameter)
        setattr(cls.update, "__signature__", endpoint_function.replace(parameters=new_parameters))

        cls.update = router.post(path="/organizations/{org_id}/update", **get_route_args(cls.update))(  # type: ignore
            cls.update
        )

    @classmethod
    def __init_get(cls, router: fastapi.APIRouter) -> None:
        endpoint_function = inspect.signature(cls.get)
        new_parameters: typing.List[inspect.Parameter] = []
        for index, (parameter_name, parameter) in enumerate(endpoint_function.parameters.items()):
            if index == 0:
                new_parameters.append(parameter.replace(default=fastapi.Depends(cls)))
            elif parameter_name == "org_id":
                new_parameters.append(parameter.replace(default=fastapi.Path(...)))
            else:
                new_parameters.append(parameter)
        setattr(cls.get, "__signature__", endpoint_function.replace(parameters=new_parameters))

        cls.get = router.get(  # type: ignore
            path="/organizations/{org_id}", response_model=Organization, **get_route_args(cls.get)
        )(cls.get)
