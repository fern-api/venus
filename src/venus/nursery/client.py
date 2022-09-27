from .resources import OwnerService


class NurseryApiClient:
    def __init__(self, origin: str):
        self.owner: OwnerService = OwnerService(origin=origin)
