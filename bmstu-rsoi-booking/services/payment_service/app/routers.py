from fastapi import APIRouter, Depends, status, Header, Response, Request, Query
from sqlalchemy.orm import Session
from database.AppDatabase import AppDatabase
from config.config import get_settings

import services as PaymentService
from schemas.responses import ResponsesEnum
from schemas.dto import PaymentInfo
from schemas.dto import EventInfoMsg
from uuid import UUID

from validator import Validator
from producer import KafkaProducer
from config.statistic_config import SERVICE_NAME, ActionType
import time

router = APIRouter(prefix='', tags=['Payment REST API operations'])
app_db = AppDatabase.app_db
settings = get_settings()


@router.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_availability():
    return Response(status_code=status.HTTP_200_OK)


@router.get(f'{settings["prefix"]}', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.PaymentInfo.value
            })
async def get_payments(data: list[str] = Query(None),
                       db: Session = Depends(app_db.get_db),
                       credentials: str = Header(alias='Authorization')):       # PaymentUids
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token)
    if not (userinfo):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    payments = await PaymentService.get_payments(data, db)
    KafkaProducer.send(EventInfoMsg(username=userinfo["username"], eventAction=ActionType.PAYMENT_INFO,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return payments


@router.post(f'{settings["prefix"]}', status_code=status.HTTP_200_OK,
            responses={
                 status.HTTP_200_OK: ResponsesEnum.PaymentInfo.value
            })
async def create_payment(payment_price: int = Header(alias='X-Payment-Price'),
                         db: Session = Depends(app_db.get_db),
                         credentials: str = Header(alias='Authorization')):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token)
    if not (userinfo):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    payment = await PaymentService.create_payment(payment_price, db)
    KafkaProducer.send(EventInfoMsg(username=userinfo["username"], eventAction=ActionType.CREATE_PAYMENT,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return ResponsesEnum.get_payment_response(payment)


@router.patch(f'{settings["prefix"]}/' + '{paymentUid}', status_code=status.HTTP_200_OK,
              responses={
                  status.HTTP_200_OK: ResponsesEnum.PaymentUpdateResponse.value
              })
async def update_payment(paymentUid: UUID,
                         data: PaymentInfo = None,
                         db: Session = Depends(app_db.get_db),
                         credentials: str = Header(alias='Authorization')):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token)
    if not (userinfo):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    payment = await PaymentService.update_payment(paymentUid, data, db)
    KafkaProducer.send(EventInfoMsg(username=userinfo["username"], eventAction=ActionType.CREATE_PAYMENT,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return ResponsesEnum.get_payment_response(payment)
