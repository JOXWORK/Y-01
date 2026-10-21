paths = [
    "session.session",
    "httpx_client.client",
    "auth_header.header",
]

pytest_plugins = list(["tests.testing_core.fixtures." + path for path in paths])
