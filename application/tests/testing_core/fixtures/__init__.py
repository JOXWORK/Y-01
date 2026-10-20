paths = [
    "session.session",
]

pytest_plugins = list(["tests.testing_core.fixtures." + path for path in paths])
