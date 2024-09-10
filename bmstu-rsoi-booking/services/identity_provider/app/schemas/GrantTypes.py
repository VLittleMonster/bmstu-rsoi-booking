from enum import Enum, unique

@unique
class GrantTypes(str, Enum):
    PASSWORD = "password"
    REFRESH_TOKEN = "refresh-token"
