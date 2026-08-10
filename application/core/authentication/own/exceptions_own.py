from fastapi_users.exceptions import FastAPIUsersException


class UserSessionInvalid(FastAPIUsersException):
    pass


class UserSessionRevoked(UserSessionInvalid):
    pass


class UserSessionNotExists(UserSessionInvalid):
    pass


class UserSessionExpires(UserSessionInvalid):
    pass


class UserSessionMaxReissueAmount(UserSessionInvalid):
    pass


class RefreshTokenRevoked(FastAPIUsersException):
    pass


class RefreshTokenNotExists(FastAPIUsersException):
    pass
