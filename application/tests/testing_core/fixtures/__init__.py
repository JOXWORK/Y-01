paths = [
    "session.session",
    "httpx_client.httpx_client",
    "auth_header.auth_header",
    "create_user.db_method",
]

pytest_plugins = list(["tests.testing_core.fixtures." + path for path in paths])
