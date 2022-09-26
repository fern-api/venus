from fastapi import APIRouter
from fastapi import Depends
from fastapi_utils.cbv import cbv

import venus.generated.server.venus_api.src.organization as fern

from venus.auth.auth0_client import Auth0Client
from venus.global_dependencies import get_auth0


router = APIRouter()


@cbv(router)
class OrganizationsService:
    @router.post("/organizations/create")
    def create_organization(
        self,
        request: fern.CreateOrganizationRequest,
        auth0_client: Auth0Client = Depends(get_auth0),
    ) -> None:
        print("Creating organization in Auth0")
        auth0_client.get().create_organization(org_id=request.organization_id)
