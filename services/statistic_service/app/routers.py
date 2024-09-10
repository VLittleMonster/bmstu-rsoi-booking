from fastapi import APIRouter, Depends, status, Header, Response, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.AppDatabase import AppDatabase
from config.config import get_settings

import services as StatisticService

from validator import Validator

router = APIRouter(prefix='', tags=['Loyalty REST API operations'])
app_db = AppDatabase.app_db
settings = get_settings()


@router.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_availability():
    return Response(status_code=status.HTTP_200_OK)


@router.get(f'{settings["prefix"]}/all')
async def get_statistic(token: str = Header(alias='Authorization', default=""),
                        db: Session = Depends(app_db.get_db)):
    token = token.replace("Bearer ", "")
    userinfo = await Validator.get_userinfo(token)
    if userinfo is None:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"msg": "Unauthorized"})
    if userinfo["role"] != "admin":
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg": "Forbidden"})
    return await StatisticService.get_statistic(db)


@router.get(f'{settings["prefix"]}/services/avg-time')
async def get_services_avg(token: str = Header(alias='Authorization', default=""),
                           db: Session = Depends(app_db.get_db)):
    token = token.replace("Bearer ", "")
    userinfo = await Validator.get_userinfo(token)
    if userinfo is None:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"msg": "Unauthorized"})
    if userinfo["role"] != "admin":
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg": "Forbidden"})
    return await StatisticService.get_services_avg_time(db)


@router.get(f'{settings["prefix"]}/queries/avg-time')
async def get_queries_avg(token: str = Header(alias='Authorization', default=""),
                          db: Session = Depends(app_db.get_db)):
    token = token.replace("Bearer ", "")
    userinfo = await Validator.get_userinfo(token)
    if userinfo is None:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"msg": "Unauthorized"})
    if userinfo["role"] != "admin":
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"msg": "Forbidden"})
    return await StatisticService.get_queries_avg_time(db)
