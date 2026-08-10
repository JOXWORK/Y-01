from core.authentication.own import BearerTransportOwn
from core.config import settings

bearer_transport = BearerTransportOwn(
    tokenUrl=settings.api.v1.prefix.bearer_transport,
)
