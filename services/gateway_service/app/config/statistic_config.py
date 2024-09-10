from enum import Enum, unique

SERVICE_NAME = "Gateway Service"


@unique
class ActionType(str, Enum):
    REGISTRATION = "registration"
    AUTHORIZATION = "authorization"
    LOGOUT = "logout"
    ALL_HOTELS = "all_hotels"
    USER_INFO = "user_info"
    LOYALTY_INFO = "loyalty_info"
    RESERVATIONS_BY_USERNAME = "reservations_by_username"
    RESERVATION_BY_UUID = "reservation_by_uuid"
    CREATE_RESERVATION = "create_reservation"
    CANCEL_RESERVATION = "cancel_reservation"
