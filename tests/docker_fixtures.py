import json

import pytest
import requests

from venus.global_dependencies import config


def is_responsive(url: str):  # type: ignore
    try:
        response = requests.get(url)
        print(response)
        if response.status_code == 204:
            return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def nursery_docker(docker_ip, docker_services):  # type: ignore
    print(config.nursery_origin + "/health")
    docker_services.wait_until_responsive(
        timeout=30.0,
        pause=1,
        check=lambda: is_responsive(config.nursery_origin + "/health"),
    )
