from enum import Enum, unique

SERVICE_NAME = "Identity Provider"


@unique
class ActionType(str, Enum):
    REGISTRATION = "registration"
    AUTHORIZATION = "authorization"
    LOGOUT = "logout"
