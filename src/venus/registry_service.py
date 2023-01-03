from fastapi import Depends
from fern.nursery.pydantic.token import RevokeTokenRequest
from fern.nursery.pydantic.token import CreateTokenRequest

import venus.generated.server.resources as fern

from venus.global_dependencies import get_nursery_client
from venus.nursery.client import NurseryApiClient
from venus.nursery.resources.token.types.get_token_metadata_request import (
    GetTokenMetadataRequest,
)
from venus.nursery_owner_data import read_nursery_org_data


class RegistryService(fern.AbstractRegistryService):
    def generate_registry_tokens(
        self,
        body: fern.GenerateRegistryTokensRequest,
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> fern.RegistryTokens:
        create_token_response = nursery_client.token.create(
            body=CreateTokenRequest(
                owner_id=body.organization_id.get_as_str(), prefix="fern"
            )
        )
        if create_token_response.ok:
            return fern.RegistryTokens(
                npm=fern.NpmRegistryToken(
                    token=create_token_response.body.token
                ),
                maven=fern.MavenRegistryToken(
                    username=body.organization_id.get_as_str(),
                    password=create_token_response.body.token,
                ),
            )
        else:
            raise Exception(
                f"Failed to generate token for org: {body.organization_id}",
                create_token_response.error,
            )

    def has_registry_permission(
        self,
        body: fern.CheckRegistryPermissionRequest,
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> bool:
        get_owner_response = nursery_client.owner.get(
            owner_id=body.organization_id.get_as_str()
        )
        if not get_owner_response.ok:
            raise Exception("Failed to load organization")
        nursery_org_data = read_nursery_org_data(get_owner_response.body.data)
        if not nursery_org_data.artifact_read_requires_token:
            return True
        elif body.token is None:
            raise Exception("Token is required to auth")
        else:
            token = body.token.visit(
                lambda npm: npm.token, lambda maven: maven.password
            )
            token_metadata_response = nursery_client.token.get_token_metadata(
                body=GetTokenMetadataRequest(token=token)
            )
            if token_metadata_response.ok:
                status = token_metadata_response.body.status.get_as_union()
                return status.type == "active"
            else:
                return False

    def revoke_token(
        self,
        body: fern.RevokeTokenRequest,
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> None:
        nursery_client.token.revoke_token(
            body=RevokeTokenRequest(token=body.token)
        )
