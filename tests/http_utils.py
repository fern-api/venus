def assert_valid_status_code(status_code: int, endpoint: str) -> None:
    if status_code >= 200 and status_code < 300:
        return None
    raise Exception(
        f"Received status_code={status_code} for endpoint={endpoint}"
    )
