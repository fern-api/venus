from ctypes import Union
from typing import Any
import pydantic


class NurseryOrgData(pydantic.BaseModel):
    auth0_id: str
    artifact_read_requires_token: bool = pydantic.Field(
        alias="artifactReadRequiresToken", default=False
    )

    class Config:
        allow_population_by_field_name = True


def read_nursery_org_data(data: Any) -> NurseryOrgData:
    if type(data) is dict:
        data_dict = dict(data)
        if "auth0_id" not in data_dict:
            raise Exception("Couldn't find auth0_id for the relevant org")
        return NurseryOrgData(
            auth0_id=data_dict["auth0_id"],
            artifact_read_requires_token=data_dict["artifactReadRequiresToken"]
            if "artifactReadRequiresToken" in data_dict
            else True,
        )
    raise Exception("Org data is not a dict that can be parsed", data)
