from models import StatisticMsg
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from schemas.dto import EventInfoDTO, EventInfoResponse, ServiceAvgTimeDTO, QueryAvgTimeDTO
from typing import List


async def add_event_info(event_dto: EventInfoDTO, db: Session):
    new_event = StatisticMsg(event_uuid=event_dto.eventUuid, username=event_dto.username,
                             event_action=event_dto.eventAction, start_time=event_dto.startTime,
                             end_time=event_dto.endTime, service_name=event_dto.serviceName)
    try:
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
    except Exception as e:
        print(f"AddingEventInfoError: {e}")


async def get_statistic(db: Session) -> List[EventInfoResponse]:
    events = list(db.query(StatisticMsg).all())
    return [event.get_event_dto() for event in events]


async def get_services_avg_time(db: Session) -> List[ServiceAvgTimeDTO]:
    avgs = db.query(StatisticMsg.service_name,
                    func.avg(StatisticMsg.end_time - StatisticMsg.start_time).label('avg_time'),
                    func.count(StatisticMsg.event_uuid))\
        .group_by(StatisticMsg.service_name).order_by("avg_time").all()

    return [ServiceAvgTimeDTO(serviceName=v.service_name, avgTime=v[1]*1000, num=v[2]) for v in avgs]


async def get_queries_avg_time(db: Session) -> List[QueryAvgTimeDTO]:
    avgs = db.query(StatisticMsg.service_name, StatisticMsg.event_action,
                    func.avg(StatisticMsg.end_time - StatisticMsg.start_time).label('avg_time'),
                    func.count(StatisticMsg.event_uuid))\
        .group_by(StatisticMsg.service_name, StatisticMsg.event_action).order_by("avg_time").all()

    return [
        QueryAvgTimeDTO(serviceName=v.service_name, eventAction=v.event_action, avgTime=v[2]*1000,
                        num=v[3]) for v in avgs
    ]
