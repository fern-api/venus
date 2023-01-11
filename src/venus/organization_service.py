import logging

from fastapi import Depends

import venus.generated.server.resources.commons as fern_commons
import venus.generated.server.resources.organization as fern

from venus.auth.auth0_client import Auth0Client
from venus.generated.server.resources.commons import UnauthorizedError
from venus.generated.server.resources.organization import AddUserToOrgRequest
from venus.generated.server.resources.organization import Organization
from venus.generated.server.security import ApiAuth
from venus.global_dependencies import get_auth0
from venus.global_dependencies import get_nursery_client
from venus.nursery.client import NurseryApiClient
from venus.nursery.resources import CreateOwnerRequest
from venus.nursery.resources.owner.types.update_owner_request import (
    UpdateOwnerRequest,
)
from venus.nursery.resources.token.types.get_token_metadata_request import (
    GetTokenMetadataRequest,
)
from venus.nursery_owner_data import NurseryOrgData
from venus.nursery_owner_data import read_nursery_org_data


logger = logging.getLogger(__name__)


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

    def is_member(
        self,
        *,
        organization_id: str,
        auth: ApiAuth,
        auth0_client: Auth0Client = Depends(get_auth0),
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> bool:
        if auth.token.startswith("fern"):
            print(auth.token, "Token starts with fern, it is a nursery token")
            try:
                owner_id = _get_owner_id_from_token(
                    auth=auth, nursery_client=nursery_client
                )
                return owner_id == organization_id
            except UnauthorizedError:
                return False
        elif self.is_valid_jwt(auth.token, auth0_client):
            print(auth.token, "Token is a valid JWT, it is a user token")
            user_id = auth0_client.get_user_id_from_token(auth.token)
            nursery_owner = _get_nursery_owner(
                owner_id=organization_id, nursery_client=nursery_client
            )
            org_ids = auth0_client.get().get_orgs_for_user(user_id=user_id)
            return nursery_owner.auth0_id in org_ids
        else:  # assume it is a legacy unprefixed nursery token
            print(
                auth.token,
                "Token neither starts with Fern or is a JWT, it is a nursery token",
            )
            try:
                owner_id = _get_owner_id_from_token(
                    auth=auth, nursery_client=nursery_client
                )
                return owner_id == organization_id
            except UnauthorizedError:
                return False

    def get(
        self,
        org_id: str,
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> fern.Organization:
        return _get_owner(owner_id=org_id, nursery_client=nursery_client)

    def get_my_organization_from_scoped_token(
        self,
        *,
        auth: ApiAuth,
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> Organization:
        owner_id = _get_owner_id_from_token(
            auth=auth, nursery_client=nursery_client
        )
        logging.debug(f"Token has owner id {owner_id}")
        return _get_owner(owner_id=owner_id, nursery_client=nursery_client)

    def add_user(
        self,
        *,
        body: AddUserToOrgRequest,
        auth: ApiAuth,
        auth0_client: Auth0Client = Depends(get_auth0),
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> None:
        user_id = auth0_client.get_user_id_from_token(auth.token)
        user_org_ids = auth0_client.get().get_orgs_for_user(user_id=user_id)
        if body.org_id.get_as_str() not in user_org_ids:
            raise UnauthorizedError()
        nursery_owner_data = _get_nursery_owner(
            owner_id=body.org_id.get_as_str(), nursery_client=nursery_client
        )
        auth0_client.get().add_user_to_org(
            user_id=user_id, org_id=nursery_owner_data.auth0_id
        )

    def is_valid_jwt(self, token: str, auth0_client: Auth0Client) -> bool:
        try:
            auth0_client.get_user_id_from_token(token=token)
            return True
        except Exception:
            return False


def _get_owner_id_from_token(
    *,
    auth: ApiAuth,
    nursery_client: NurseryApiClient = Depends(get_nursery_client),
) -> str:
    get_token_metadata_response = nursery_client.token.get_token_metadata(
        body=GetTokenMetadataRequest(token=auth.token)
    )
    if not get_token_metadata_response.ok:
        raise fern_commons.UnauthorizedError()
    token_status = get_token_metadata_response.body.status.get_as_union()
    if token_status.type == "expired" or token_status.type == "revoked":
        raise fern_commons.UnauthorizedError()
    owner_id = get_token_metadata_response.body.owner_id
    return owner_id


def _get_owner(
    *, owner_id: str, nursery_client: NurseryApiClient
) -> fern.Organization:
    org_data = _get_nursery_owner(
        owner_id=owner_id, nursery_client=nursery_client
    )
    return fern.Organization(
        organization_id=fern_commons.OrganizationId.from_str(owner_id),
        artifact_read_requires_token=org_data.artifact_read_requires_token,
    )


def _get_nursery_owner(
    *, owner_id: str, nursery_client: NurseryApiClient
) -> NurseryOrgData:
    logging.debug(f"Getting owner with id {owner_id}")
    get_owner_response = nursery_client.owner.get(owner_id=owner_id)
    if not get_owner_response.ok:
        raise Exception(
            f"Error while retrieving owner from nursery with id={owner_id}",
            get_owner_response.error,
        )
    return read_nursery_org_data(get_owner_response.body.data)
