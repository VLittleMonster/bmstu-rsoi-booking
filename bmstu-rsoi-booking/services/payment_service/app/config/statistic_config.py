from enum import Enum, unique

SERVICE_NAME = "Payment Service"


@unique
class ActionType(str, Enum):
    PAYMENT_INFO = "payment_info"
    CREATE_PAYMENT = "create_payment"
    UPDATE_PAYMENT = "update_payment"
