from sqlalchemy import FLOAT, Column, VARCHAR
from typing import Final
from database.database import Base
from schemas.dto import EventInfoResponse
import datetime

DISCOUNT_BY_STATUS: Final = {'BRONZE': 5, 'SILVER': 7, 'GOLD': 10}  # статусы и размеры скидок в процентах


class StatisticMsg(Base):
    __tablename__ = 'statistics'
    __table_args__ = {
        'extend_existing': True
    }

    event_uuid = Column(VARCHAR(), nullable=False, primary_key=True)
    username = Column(VARCHAR(80), nullable=False)
    event_action = Column(VARCHAR(80), nullable=False)
    start_time = Column(FLOAT(), nullable=False)
    end_time = Column(FLOAT(), nullable=False)
    service_name = Column(VARCHAR(80), nullable=False)

    def __init__(self, event_uuid: str, username: str, event_action: str,
                 start_time: float, end_time: float, service_name: str):
        self.event_uuid = event_uuid
        self.username = username
        self.event_action = event_action
        self.start_time = start_time + 3*3600   # GMT+03 dim
        self.end_time = end_time + 3*3600       # GMT+03 dim
        self.service_name = service_name

    def get_event_dto(self):
        return EventInfoResponse(
            eventUuid=self.event_uuid,
            username=self.username,
            eventAction=self.event_action,
            startTime=str(datetime.datetime.fromtimestamp(self.start_time)),
            endTime=str(datetime.datetime.fromtimestamp(self.end_time)),
            serviceName=self.service_name
        )
