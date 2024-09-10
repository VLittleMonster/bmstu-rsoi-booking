from fastapi import APIRouter, Depends, status, Header, Response, Request
from sqlalchemy.orm import Session
from database.AppDatabase import AppDatabase
from config.config import get_settings

import services as LoyaltyService
from schemas.responses import ResponsesEnum
from schemas.dto import LoyaltyInfoRequest, EventInfoMsg

from validator import Validator
from producer import KafkaProducer
from config.statistic_config import SERVICE_NAME, ActionType
import time

router = APIRouter(prefix='', tags=['Loyalty REST API operations'])
app_db = AppDatabase.app_db
settings = get_settings()


@router.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_availability():
    return Response(status_code=status.HTTP_200_OK)


@router.get(f'{settings["prefix"]}/', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.LoyaltyInfoResponse.value
            })
async def get_loyalty(credentials: str = Header(alias='Authorization'), db: Session = Depends(app_db.get_db)):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.get_userinfo(token)
    if userinfo is None:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    loyalty = await LoyaltyService.get_loyalty(userinfo["username"], db)
    KafkaProducer.send(EventInfoMsg(username=userinfo["username"], eventAction=ActionType.LOYALTY_INFO,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return ResponsesEnum.get_loyalty_response(loyalty)


@router.patch(f'{settings["prefix"]}/', status_code=status.HTTP_200_OK,
              responses={
                  status.HTTP_200_OK: ResponsesEnum.LoyaltyUpdateResponse.value
              })
async def update_loyalty(data: LoyaltyInfoRequest,
                         credentials: str = Header(alias='Authorization'),
                         db: Session = Depends(app_db.get_db)):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.get_userinfo(token)
    if userinfo is None:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    await LoyaltyService.update_loyalty(data, userinfo["username"], db)
    KafkaProducer.send(EventInfoMsg(username=userinfo["username"], eventAction=ActionType.UPDATE_LOYALTY_INFO,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return Response(status_code=status.HTTP_200_OK)
