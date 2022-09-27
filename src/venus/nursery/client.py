from .resources import OwnerService
from .resources import TokenService


class NurseryApiClient:
    def __init__(self, origin: str):
        self.owner: OwnerService = OwnerService(origin=origin)
        self.token: TokenService = TokenService(origin=origin)
