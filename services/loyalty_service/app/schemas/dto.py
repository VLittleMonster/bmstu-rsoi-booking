from pydantic import BaseModel


class LoyaltyInfoResponse(BaseModel):
    status: str
    discount: int
    reservationCount: int


class LoyaltyInfoRequest(BaseModel):
    reservationCountOperation: int | None = None


class EventInfoMsg(BaseModel):
    eventUuid: str | None = None
    username: str
    eventAction: str
    startTime: float
    endTime: float
    serviceName: str
