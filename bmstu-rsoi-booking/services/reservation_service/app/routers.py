from fastapi import APIRouter, Depends, status, Header, Response, Request
from sqlalchemy.orm import Session
from database.AppDatabase import AppDatabase
from config.config import get_settings

import services as ReservationService
from schemas.responses import ResponsesEnum
from schemas.dto import UpdateReservation
from schemas.dto import CreateReservationRequest, EventInfoMsg
from uuid import UUID

from validator import Validator
from producer import KafkaProducer
from config.statistic_config import SERVICE_NAME, ActionType
import time

router = APIRouter(prefix='', tags=['Reservation REST API operations'])
app_db = AppDatabase.app_db
settings = get_settings()


@router.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_availability():
    return Response(status_code=status.HTTP_200_OK)


@router.get(f'{settings["prefix"]}/hotels', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.PaginationResponse.value
            })
async def get_hotels(page: int = 0, size: int = 0,
                     db: Session = Depends(app_db.get_db),
                     credentials: str = Header(alias='Authorization')):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token)
    if not (userinfo):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    hotels = await ReservationService.get_hotels(page, size, db)
    KafkaProducer.send(EventInfoMsg(username=userinfo["username"], eventAction=ActionType.ALL_HOTELS,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return hotels


@router.get(f'{settings["prefix"]}/hotels/' + '{hotelUid}', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.HotelResponse.value
            })
async def get_hotel(hotelUid: UUID,
                    db: Session = Depends(app_db.get_db),
                    credentials: str = Header(alias='Authorization')):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token)
    if not (userinfo):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    hotel = await ReservationService.get_hotel(hotelUid, db)
    KafkaProducer.send(EventInfoMsg(username=userinfo["username"], eventAction=ActionType.HOTEL_BY_UUID,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return ResponsesEnum.get_hotel_response(hotel)


@router.get(f'{settings["prefix"]}/reservations', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.ReservationResponse.value
            })
async def get_reservations(credentials: str = Header(alias='Authorization'),
                           db: Session = Depends(app_db.get_db)):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.get_userinfo(token)
    if userinfo is None:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    reservations = await ReservationService.get_reservations(userinfo["username"], db)
    KafkaProducer.send(EventInfoMsg(username=userinfo["username"], eventAction=ActionType.RESERVATIONS_BY_USERNAME,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return reservations


@router.get(f'{settings["prefix"]}/reservations/' + '{reservationUid}', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.ReservationResponse.value
            })
async def get_reservation(reservationUid: UUID,
                          credentials: str = Header(alias='Authorization'),
                          db: Session = Depends(app_db.get_db)):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.get_userinfo(token)
    if userinfo is None:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    reservation = await ReservationService.get_reservation(reservationUid, userinfo["username"], db)
    KafkaProducer.send(EventInfoMsg(username=userinfo["username"], eventAction=ActionType.RESERVATION_BY_UUID,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return reservation


@router.post(f'{settings["prefix"]}/reservations', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.CreateReservationResponse.value
            })
async def create_reservation(credentials: str = Header(alias='Authorization'),
                             data: CreateReservationRequest = None,
                             db: Session = Depends(app_db.get_db)):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.get_userinfo(token)
    if userinfo is None:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    reservation = await ReservationService.create_reservation(userinfo["username"], data, db)
    KafkaProducer.send(EventInfoMsg(username=userinfo["username"], eventAction=ActionType.CREATE_RESERVATION,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return reservation


@router.patch(f'{settings["prefix"]}/reservations/' + '{reservationUid}', status_code=status.HTTP_200_OK,
              responses={
                status.HTTP_200_OK: ResponsesEnum.ReservationResponse.value
              })
async def update_reservation(reservationUid: UUID,
                             data: UpdateReservation = None,
                             credentials: str = Header(alias='Authorization'),
                             db: Session = Depends(app_db.get_db)):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.get_userinfo(token)
    if userinfo is None:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    reservation = await ReservationService.update_reservation(reservationUid, data, userinfo["username"], db)
    KafkaProducer.send(EventInfoMsg(username=userinfo["username"], eventAction=ActionType.CANCEL_RESERVATION,
                                    startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return reservation.model_dump()
