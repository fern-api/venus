from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from .generated.server.venus_api.src.registry import GenerateRegistryTokensRequest, RegistryTokens, CheckRegistryPermissionRequest

router = InferringRouter() 

@cbv(router)
class RegistryService(): 
  
  @router.post("/registry/generate-tokens")
  def generate_registry_tokens(self, request: GenerateRegistryTokensRequest) -> RegistryTokens: 
    print("Generating registry tokens")
    pass
  
  @router.post("/registry/check-permissions")
  def has_registry_permission(self, request: CheckRegistryPermissionRequest) -> bool: 
    print("Has registry permissions")
    pass