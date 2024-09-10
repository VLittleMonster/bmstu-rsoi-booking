from enum import Enum, unique

SERVICE_NAME = "Loyalty Service"


@unique
class ActionType(str, Enum):
    LOYALTY_INFO = "loyalty_info"
    UPDATE_LOYALTY_INFO = "update_loyalty_info"
