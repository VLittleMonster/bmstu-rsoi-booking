from pydantic import BaseModel
from typing import Literal, List
from uuid import UUID


class PaymentInfo(BaseModel):
    status: Literal['PAID', 'CANCELED'] | None = None
    price: float | None = None
    uid: UUID | None = None


class PaymentUids(BaseModel):
    uid: UUID


class EventInfoMsg(BaseModel):
    eventUuid: str | None = None
    username: str
    eventAction: str
    startTime: float
    endTime: float
    serviceName: str
