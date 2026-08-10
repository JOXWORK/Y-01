from core.authentication import bearer_transport
from core.authentication.own import AuthenticationBackendOwn

from .get_database_strategy import get_database_strategy

auth_backend = AuthenticationBackendOwn(
    name="user-session-token-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
