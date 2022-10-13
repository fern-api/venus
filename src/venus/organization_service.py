from fastapi import Depends

import venus.generated.server.resources.commons as fern_commons
import venus.generated.server.resources.organization as fern

from venus.auth.auth0_client import Auth0Client
from venus.global_dependencies import get_auth0
from venus.global_dependencies import get_nursery_client
from venus.nursery.client import NurseryApiClient
from venus.nursery.resources import CreateOwnerRequest
from venus.nursery.resources.owner.types.update_owner_request import (
    UpdateOwnerRequest,
)
from venus.nursery_owner_data import NurseryOrgData
from venus.nursery_owner_data import read_nursery_org_data


class OrganizationsService(fern.AbstractOrganizationService):
    def create(
        self,
        body: fern.CreateOrganizationRequest,
        auth0_client: Auth0Client = Depends(get_auth0),
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> None:
        auth0_org_id = auth0_client.get().create_organization(
            org_id=body.organization_id.get_as_str()
        )
        nursery_org_data = NurseryOrgData(auth0_id=auth0_org_id)
        nursery_client.owner.create(
            body=CreateOwnerRequest(
                owner_id=body.organization_id.get_as_str(),
                data=nursery_org_data,
            )
        )

    def update(
        self,
        org_id: str,
        body: fern.UpdateOrganizationRequest,
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
            body.artifact_read_requires_token
        )
        owner_update_response = nursery_client.owner.update(
            owner_id=org_id,
            body=UpdateOwnerRequest(data=org_data),
        )
        if not owner_update_response.ok:
            raise Exception(
                "Encountered error while updating org",
                owner_update_response.error,
            )

    def get(
        self,
        org_id: str,
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> fern.Organization:
        get_owner_response = nursery_client.owner.get(owner_id=org_id)
        if not get_owner_response.ok:
            raise Exception(
                "Encountered error while retrieving org",
                get_owner_response.error,
            )
        org_data = read_nursery_org_data(get_owner_response.body.data)
        return fern.Organization(
            organization_id=fern_commons.OrganizationId.from_str(org_id),
            artifact_read_requires_token=org_data.artifact_read_requires_token,
        )
