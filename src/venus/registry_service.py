from fastapi import APIRouter
from fastapi import Depends
from fastapi_utils.cbv import cbv

import venus.generated.server.venus_api.src.registry as fern

from venus.global_dependencies import get_nursery_client
from venus.nursery.client import NurseryApiClient
from venus.nursery.resources.token.types.create_token_request import (
    CreateTokenRequest,
)
from venus.nursery.resources.token.types.get_token_metadata_request import (
    GetTokenMetadataRequest,
)


router = APIRouter()


@cbv(router)
class RegistryService:
    @router.post("/registry/generate-tokens")
    def generate_registry_tokens(
        self,
        request: fern.GenerateRegistryTokensRequest,
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> fern.RegistryTokens:
        create_token_response = nursery_client.token.create(
            body=CreateTokenRequest(owner_id=request.organization_id)
        )
        if create_token_response.ok:
            return fern.RegistryTokens(
                npm=fern.NpmRegistryToken(
                    token=create_token_response.body.token
                ),
                maven=fern.MavenRegistryToken(
                    username=request.organization_id,
                    password=create_token_response.body.token,
                ),
            )
        else:
            raise Exception(
                f"Failed to generate token for org: {request.organization_id}",
                create_token_response.error,
            )

    @router.post("/registry/check-permissions")
    def has_registry_permission(
        self,
        request: fern.CheckRegistryPermissionRequest,
        nursery_client: NurseryApiClient = Depends(get_nursery_client),
    ) -> bool:
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
