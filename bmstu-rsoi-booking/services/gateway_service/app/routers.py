from fastapi import APIRouter, status, Header, Request, Form
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from uuid import UUID
import time

import services as GatewayService
import schemas.dto as schemas
from schemas.responses import ResponsesEnum
from config.config import get_settings

from validator import Validator
from producer import KafkaProducer
from config.statistic_config import SERVICE_NAME, ActionType

router = APIRouter(prefix='', tags=['Gateway API'])
settings = get_settings()


@router.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_availability():
    return Response(status_code=status.HTTP_200_OK)


@router.get(f'{settings["prefix"]}/hotels', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.PaginationResponse.value
            })
async def get_all_hotels(page: int = 0, size: int = 0, credentials: str = Header(alias='Authorization', default="")):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token, leeway=0)
    if not (userinfo):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=schemas.ErrorResponse(message='Unauthorized').model_dump())
    resp = await GatewayService.get_all_hotels(page, size, token)
    KafkaProducer.send(schemas.EventInfoMsg(username=userinfo["username"], eventAction=ActionType.ALL_HOTELS,
                                            startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return resp


@router.get(f'{settings["prefix"]}/me', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.UserInfoResponse.value
            })
async def get_user_info(credentials: str = Header(alias='Authorization', default="")):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token, leeway=0)
    if not (userinfo):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=schemas.ErrorResponse(message='Unauthorized').model_dump())
    resp = await GatewayService.get_user_info(token, userinfo)
    KafkaProducer.send(schemas.EventInfoMsg(username=userinfo["username"], eventAction=ActionType.USER_INFO,
                                            startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return resp


@router.get(f'{settings["prefix"]}/loyalty', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.LoyaltyInfoResponse.value
            })
async def get_loyalty(credentials: str = Header(alias='Authorization', default="")):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token, leeway=0)
    if not (userinfo):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=schemas.ErrorResponse(message='Unauthorized').model_dump())
    resp = await GatewayService.get_loyalty(token)
    KafkaProducer.send(schemas.EventInfoMsg(username=userinfo["username"], eventAction=ActionType.LOYALTY_INFO,
                                            startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return resp


@router.get(f'{settings["prefix"]}/reservations', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.ReservationsResponse.value
            })
async def get_reservations(credentials: str = Header(alias='Authorization', default="")):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token, leeway=0)
    if not (userinfo):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=schemas.ErrorResponse(message='Unauthorized').model_dump())
    resp = await GatewayService.get_reservations(token)
    KafkaProducer.send(schemas.EventInfoMsg(username=userinfo["username"], eventAction=ActionType.RESERVATIONS_BY_USERNAME,
                                            startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return resp


@router.get(f'{settings["prefix"]}/reservations/' + '{reservationUid}', status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponsesEnum.ReservationResponse.value,
                status.HTTP_404_NOT_FOUND: ResponsesEnum.ErrorResponse.value
            })
async def get_reservation_by_uid(reservationUid: UUID, credentials: str = Header(alias='Authorization', default="")):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token, leeway=0)
    if not (userinfo):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=schemas.ErrorResponse(message='Unauthorized').model_dump())
    reservation = await GatewayService.get_reservation_by_uid(reservationUid, token)
    if reservation is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=schemas.ErrorResponse().model_dump())
    KafkaProducer.send(schemas.EventInfoMsg(username=userinfo["username"], eventAction=ActionType.RESERVATION_BY_UUID,
                                            startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return reservation


@router.post(f'{settings["prefix"]}/reservations', status_code=status.HTTP_200_OK,
             responses={
                 status.HTTP_200_OK: ResponsesEnum.CreateReservationResponse.value,
                 status.HTTP_400_BAD_REQUEST: ResponsesEnum.ValidationErrorResponse.value
             })
async def create_reservation(reservRequest: schemas.CreateReservationRequest,
                             credentials: str = Header(alias='Authorization', default="")):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token, leeway=0)
    if not (userinfo):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=schemas.ErrorResponse(message='Unauthorized').model_dump())
    try:
        reservation = await GatewayService.create_reservation(reservRequest, token)
    except RequestValidationError as exc:
        details = [schemas.ErrorDescription(
            field=e["field"],
            error=e["msg"]
        ) for e in jsonable_encoder(exc.errors())]

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=schemas.ValidationErrorResponse(
            message='Invalid request',
            errors=list(details)
        ).model_dump())
    KafkaProducer.send(schemas.EventInfoMsg(username=userinfo["username"], eventAction=ActionType.CREATE_RESERVATION,
                                            startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return reservation


@router.delete(f'{settings["prefix"]}/reservations/' + '{reservationUid}', status_code=status.HTTP_204_NO_CONTENT,
               responses={
                   status.HTTP_404_NOT_FOUND: ResponsesEnum.ErrorResponse.value
               })
async def delete_reservation(reservationUid: UUID, credentials: str = Header(alias='Authorization', default="")):
    start_time = time.time()
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token, leeway=0)
    if not (userinfo):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=schemas.ErrorResponse(message='Unauthorized').model_dump())

    resp = await GatewayService.delete_reservation(reservationUid, token)
    KafkaProducer.send(schemas.EventInfoMsg(username=userinfo["username"], eventAction=ActionType.CANCEL_RESERVATION,
                                            startTime=start_time, endTime=time.time(), serviceName=SERVICE_NAME))
    return resp


@router.post(f'{settings["prefix"]}/register')
async def register_user(data: Request):
    resp = await GatewayService.register_user(request=data)
    return resp


@router.post(f'{settings["prefix"]}/oauth/token')
async def auth_user(auth_request: schemas.AuthenticationRequest, refresh_token: str = Header(alias='Authorization', default="")):
    resp = await GatewayService.auth_user(schemas.AuthenticationRequest(
        scope=auth_request.scope,
        grant_type=auth_request.grant_type,
        username=auth_request.username,
        password=auth_request.password,
        refresh_token=refresh_token
    ))
    return resp


@router.post(f'{settings["prefix"]}/oauth/revoke', status_code=status.HTTP_200_OK, responses={})
async def logout(request: Request):
    await GatewayService.logout(request)


@router.get(f'{settings["prefix"]}/statistic/all')
async def get_statistic(credentials: str = Header(alias='Authorization', default="")):
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token, leeway=0)
    if not (userinfo):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=schemas.ErrorResponse(message='Unauthorized').model_dump())
    return await GatewayService.get_statistic(credentials)


@router.get(f'{settings["prefix"]}/statistic/services/avg-time')
async def get_service_avg(credentials: str = Header(alias='Authorization', default="")):
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token, leeway=0)
    if not (userinfo):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=schemas.ErrorResponse(message='Unauthorized').model_dump())
    return await GatewayService.get_service_avg(credentials)


@router.get(f'{settings["prefix"]}/statistic/queries/avg-time')
async def get_query_avg(credentials: str = Header(alias='Authorization', default="")):
    token = credentials.replace("Bearer ", "")
    userinfo = await Validator.validate_token(token, leeway=0)
    if not (userinfo):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=schemas.ErrorResponse(message='Unauthorized').model_dump())
    return await GatewayService.get_query_avg(credentials)
