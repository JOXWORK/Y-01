from secrets import token_hex

mixin = token_hex(8)

username = f"test_{mixin}@e.com"
password = "qwerty"

credentials = {
    "register": {
        "email": username,
        "password": password,
        "is_active": True,
        "is_superuser": True,
        "is_verified": True,
    },
    "login": {
        "username": username,
        "password": password,
    },
}

user_credentials = {
    "username": "user@e.com",
    "password": "ABBAB",
}
