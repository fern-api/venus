import os

import pytest


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig) -> str:  # type: ignore
    return os.path.join(str(pytestconfig.rootdir), "compose-ete.yml")
