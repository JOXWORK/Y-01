from enum import Enum


class ReissueErrorDetails(str, Enum):
    BAD_REFRESH_TOKEN = "BAD_REFRESH_TOKEN"
