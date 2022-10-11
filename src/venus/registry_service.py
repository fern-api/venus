from fastapi import Depends

import venus.generated.server.resources as fern

from venus.global_dependencies import get_nursery_client
from venus.nursery.client import NurseryApiClient
from venus.nursery.resources.token.types.create_token_request import (
    CreateTokenRequest,
)
from venus.nursery.resources.token.types.get_token_metadata_request import (
    GetTokenMetadataRequest,
)
from venus.nursery_owner_data import read_nursery_org_data


class RegistryService(fern.AbstractRegistryService):
    def generate_registry_tokens(
        self,
        request: fern.GenerateRegistryTokensRequest,
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> fern.RegistryTokens:
        create_token_response = nursery_client.token.create(
            body=CreateTokenRequest(
                owner_id=request.organization_id.get_as_str()
            )
        )
        if create_token_response.ok:
            return fern.RegistryTokens(
                npm=fern.NpmRegistryToken(
                    token=create_token_response.body.token
                ),
                maven=fern.MavenRegistryToken(
                    username=request.organization_id.get_as_str(),
                    password=create_token_response.body.token,
                ),
            )
        else:
            raise Exception(
                f"Failed to generate token for org: {request.organization_id}",
                create_token_response.error,
            )

    def has_registry_permission(
        self,
        request: fern.CheckRegistryPermissionRequest,
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> bool:
        get_owner_response = nursery_client.owner.get(
            owner_id=request.organization_id.get_as_str()
        )
        if not get_owner_response.ok:
            raise Exception("Failed to load organization")
        nursery_org_data = read_nursery_org_data(get_owner_response.body.data)
        if not nursery_org_data.artifact_read_requires_token:
            return True
        elif request.token is None:
            raise Exception("Token is required to auth")
        else:
            token = request.token.visit(
                lambda npm: npm.token, lambda maven: maven.password
            )
            token_metadata_response = nursery_client.token.get_token_metadata(
                body=GetTokenMetadataRequest(token=token)
            )
            if token_metadata_response.ok:
                return True
            else:
                return False
