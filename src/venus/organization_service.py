from fastapi import APIRouter
from fastapi import Depends
from fastapi_utils.cbv import cbv

import venus.generated.server.venus_api.src.organization as fern
import venus.generated.server.venus_api.src.commons as fern_commons

from venus.auth.auth0_client import Auth0Client
from venus.global_dependencies import get_auth0
from venus.global_dependencies import get_nursery_client
from venus.nursery.client import NurseryApiClient
from venus.nursery.resources import CreateOwnerRequest
from venus.nursery.resources.owner.types.update_owner_request import (
    UpdateOwnerRequest,
)
from venus.nursery_owner_data import NurseryOrgData, read_nursery_org_data


router = APIRouter()


@cbv(router)
class OrganizationsService:
    @router.post("/organizations/create")
    def create(
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

    @router.post("/organizations/{org_id}/update")
    def update(
        self,
        org_id: fern_commons.OrganizationId,
        request: fern.UpdateOrganizationRequest,
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> None:
        get_owner_response = nursery_client.owner.get(owner_id=org_id)
        if not get_owner_response.ok:
            raise Exception(
                "Encountered error while retrieving org",
                get_owner_response.error,
            )
        org_data = read_nursery_org_data(get_owner_response.body.data)
        org_data.artifact_read_requires_token = (
            request.artifact_read_requires_token
        )
        owner_update_response = nursery_client.owner.update(
            owner_id=org_id, body=UpdateOwnerRequest(data=org_data)
        )
        if not owner_update_response.ok:
            raise Exception(
                "Encountered error while updating org",
                owner_update_response.error,
            )
