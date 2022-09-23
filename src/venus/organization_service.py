from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

import venus.generated.server.venus_api.src.organization as fern

router = InferringRouter()


@cbv(router)
class OrganizationsService:
    @router.post("/organizations/create")
    def create_organization(self, request: fern.CreateOrganizationRequest) -> None:
        print("Creating organization")
