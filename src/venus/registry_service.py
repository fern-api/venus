from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
import venus.generated.server.venus_api.src.registry as fern

router = InferringRouter() 

@cbv(router)
class RegistryService(): 
  
  @router.post("/registry/generate-tokens")
  def generate_registry_tokens(self, request: fern.GenerateRegistryTokensRequest) -> fern.RegistryTokens: 
    print("Generating registry tokens")
    return fern.RegistryTokens(
      npm=fern.NpmRegistryToken(token="fake"), 
      maven=fern.MavenRegistryToken(username="fake", password="fake"))
  
  @router.post("/registry/check-permissions")
  def has_registry_permission(self, request: fern.CheckRegistryPermissionRequest) -> bool: 
    print("Has registry permissions")
    return True