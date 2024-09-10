from enum import Enum, unique

@unique
class ScopeTypes(str, Enum):
    OPENID = "openid"
    PROFILE = "profile"
    EMAIL = "email"
