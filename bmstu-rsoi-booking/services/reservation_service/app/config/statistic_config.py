from enum import Enum, unique

SERVICE_NAME = "Reservation Service"


@unique
class ActionType(str, Enum):
    ALL_HOTELS = "all_hotels"
    HOTEL_BY_UUID = "hotel_by_uuid"
    RESERVATIONS_BY_USERNAME = "reservations_by_username"
    RESERVATION_BY_UUID = "reservation_by_uuid"
    CREATE_RESERVATION = "create_reservation"
    CANCEL_RESERVATION = "cancel_reservation"
