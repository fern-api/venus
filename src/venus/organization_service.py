from fastapi import APIRouter
from fastapi import Depends
from fastapi_utils.cbv import cbv

import venus.generated.server.venus_api.src.organization as fern

from venus.auth.auth0_client import Auth0Client
from venus.global_dependencies import get_auth0
from venus.global_dependencies import get_nursery_client
from venus.nursery.client import NurseryApiClient
from venus.nursery.resources.owner.types.create_owner_request import \
    CreateOwnerRequest
from venus.nursery_owner_data import NurseryOrgData


router = APIRouter()


@cbv(router)
class OrganizationsService:
    @router.post("/organizations/create")
    def create_organization(
        self,
        request: fern.CreateOrganizationRequest,
        auth0_client: Auth0Client = Depends(get_auth0),
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> None:
        auth0_org_id = auth0_client.get().create_organization(
            org_id=request.organization_id
        )
        nursery_org_data = NurseryOrgData(auth0_id=auth0_org_id)
        nursery_client.owner.create(
            body=CreateOwnerRequest(
                owner_id=request.organization_id, data=nursery_org_data
            )
        )
