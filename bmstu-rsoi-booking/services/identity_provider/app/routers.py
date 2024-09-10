from fastapi import APIRouter, Depends, status, Header, Response, Request, Form
from sqlalchemy.orm import Session
from database.AppDatabase import AppDatabase
from config.config import get_settings
import time

import services as IdentityService
from schemas.responses import ResponsesEnum
from schemas.dto import RegisterUserRequest, AuthenticationRequest, EventInfoMsg

from validator import Validator
from producer import KafkaProducer
from config.statistic_config import SERVICE_NAME, ActionType

router = APIRouter(prefix='', tags=['Loyalty REST API operations'])
app_db = AppDatabase.app_db
settings = get_settings()


@router.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_availability():
    return Response(status_code=status.HTTP_200_OK)


@router.get(f'/.well-known/jwks.json', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.JWKsResponse.value
            })
async def get_jwks(db: Session = Depends(app_db.get_db)):
    return await IdentityService.get_jwks(db)


@router.post(f'{settings["prefix"]}/register', status_code=status.HTTP_200_OK,
             responses={
                 status.HTTP_200_OK: ResponsesEnum.TokenResponse.value
             })
async def register_user(data: RegisterUserRequest,
                        db: Session = Depends(app_db.get_db)):
    start_time = time.time()
    resp = await IdentityService.register_user(user_info=data, db=db)
    KafkaProducer.send(EventInfoMsg(username=data.username, eventAction=ActionType.REGISTRATION,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return resp


@router.post(f'{settings["prefix"]}/oauth/token', status_code=status.HTTP_200_OK,
             responses={
                 status.HTTP_200_OK: ResponsesEnum.TokenResponse.value
             })
async def auth_user(request: AuthenticationRequest = None,
                    db: Session = Depends(app_db.get_db)):
    start_time = time.time()
    request.refresh_token = request.refresh_token.replace("Bearer ", "")

    resp = await IdentityService.auth_user(request, db)

    username = request.username if request.username != "" else "-"
    KafkaProducer.send(EventInfoMsg(username=username, eventAction=ActionType.AUTHORIZATION,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return resp


@router.post(f'{settings["prefix"]}/oauth/revoke', status_code=status.HTTP_200_OK,
             responses={
                 status.HTTP_200_OK: ResponsesEnum.TokenResponse.value
             })
async def logout(refresh_token: str = Header(alias='Authorization', default=""),
                 db: Session = Depends(app_db.get_db)):
    start_time = time.time()
    await IdentityService.logout(refresh_token.replace("Bearer ", ""), db)
    KafkaProducer.send(EventInfoMsg(username="-", eventAction=ActionType.LOGOUT,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
