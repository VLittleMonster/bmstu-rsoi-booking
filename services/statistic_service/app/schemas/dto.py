from pydantic import BaseModel


class EventInfoDTO(BaseModel):
    eventUuid: str
    username: str
    eventAction: str
    startTime: float
    endTime: float
    serviceName: str


class EventInfoResponse(BaseModel):
    eventUuid: str
    username: str
    eventAction: str
    startTime: str
    endTime: str
    serviceName: str


class ServiceAvgTimeDTO(BaseModel):
    serviceName: str
    num: int
    avgTime: float


class QueryAvgTimeDTO(BaseModel):
    serviceName: str
    eventAction: str
    num: int
    avgTime: float
