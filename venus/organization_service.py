from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from .generated.server.venus_api.src.organization import CreateOrganizationRequest

router = InferringRouter() 

@cbv(router)
class OrganizationsService(): 
  
  @router.post("/organizations/create")
  def create_organization(self, request: CreateOrganizationRequest) -> None: 
    print("Creating organization")
    pass
  