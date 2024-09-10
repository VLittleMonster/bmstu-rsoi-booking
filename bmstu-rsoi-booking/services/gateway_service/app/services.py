from fastapi import status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response, JSONResponse
from config.config import get_settings
from typing import Final
from schemas import dto as schemas
import serviceRequests
from uuid import UUID

import asyncio

username_in_header: Final = 'X-User-Name'
settings = get_settings()


def is_response(obj):
    if type(obj) == type(Response()) or type(obj) == type(JSONResponse(content={})):
        return True
    return False


async def get_all_hotels(page: int, size: int, token: str):
    url = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}{settings['prefix']}" \
          f"/hotels?page={page}&size={size}"
    resp = await serviceRequests.get(url, headers={'Authorization': f"Bearer {token}"})
    if resp is None or (resp != None and resp.status_code >= 500):
        return JSONResponse(status_code=503, content=schemas.UnavailableService(message="Reservation Service unavailable")
                            .model_dump())
    elif resp != None and resp.status_code == status.HTTP_401_UNAUTHORIZED:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=schemas.ErrorResponse(message='Unauthorized').model_dump())
    return resp.json()


async def get_user_info(token: str, userinfo: dict):
    [loyalty_response, reservation_response] = await asyncio.gather(get_loyalty(token), get_reservations(token))

    if is_response(reservation_response):
        if reservation_response.status_code >= 500:
            return JSONResponse(status_code=503, content=schemas.UnavailableService(message="Reservation Service unavailable")
                                .model_dump())
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())
    if is_response(loyalty_response):
        if loyalty_response.status_code >= 500:
            loyalty_response = {}
        else:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())

    profile = schemas.UserProfile(name=userinfo["first_name"],
                                  surname=userinfo["last_name"],
                                  patronymic=userinfo["patronymic"],
                                  phoneNumber=userinfo["phone_number"])
    return schemas.UserInfoResponse(profile=profile, reservations=reservation_response, loyalty=loyalty_response)


async def get_reservations(token: str):
    url_reserv_serv = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}" \
                      f"{settings['prefix']}/reservations"
    url_payment_serv = f"http://{settings['payment_serv_host']}:{settings['payment_serv_port']}{settings['prefix']}" \
                       f"/payments"
    resp = await serviceRequests.get(url_reserv_serv, headers={'Authorization': f"Bearer {token}"})
    if resp is None or (resp != None and resp.status_code >= 500):
        return JSONResponse(status_code=503, content=schemas.UnavailableService(message="Reservation Service unavailable")
                            .model_dump())
    elif resp is not None and resp.status_code == status.HTTP_401_UNAUTHORIZED:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=schemas.ErrorResponse(message='Unauthorized').model_dump())

    reservation_responses = resp.json()
    pay_uuids = []
    for res in reservation_responses:
        pay_uuids.append(res['paymentUid'])
    print(pay_uuids)
    params = {'data': pay_uuids}
    resp = await serviceRequests.get(url_payment_serv, params=params, headers={'Authorization': f"Bearer {token}"})
    print(resp.url)
    print(resp)

    payment_responses = []
    if resp is not None and resp.status_code == status.HTTP_200_OK:
        payment_responses = resp.json()
    elif resp is not None and resp.status_code == status.HTTP_401_UNAUTHORIZED:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=schemas.ErrorResponse(message='Unauthorized').model_dump())

    res = []
    for i in range(len(reservation_responses)):
        res.append(schemas.ReservationResponse(
            reservationUid=reservation_responses[i]['reservationUid'],
            hotel=reservation_responses[i]['hotel'],
            startDate=reservation_responses[i]['startDate'],
            endDate=reservation_responses[i]['endDate'],
            status=reservation_responses[i]['status'],
            payment={} if len(payment_responses) <= 0 else schemas.PaymentInfo(
                status=payment_responses[i]['status'],
                price=payment_responses[i]['price']
            )
        ))
    return res


async def get_reservation_by_uid(reservaionUid: UUID, token: str):
    url_reserv_serv = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}" \
                      f"{settings['prefix']}/reservations/{reservaionUid}"
    url_payment_serv = f"http://{settings['payment_serv_host']}:{settings['payment_serv_port']}{settings['prefix']}" \
                       f"/payments"
    reservation_response = await serviceRequests.get(url_reserv_serv, headers={'Authorization': f"Bearer {token}"})
    if reservation_response is None or reservation_response.status_code != status.HTTP_200_OK:
        if reservation_response is None or reservation_response.status_code >= 500:
            return JSONResponse(status_code=503, content=schemas.UnavailableService(message="Reservation Service unavailable")
                            .model_dump())
        elif reservation_response.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=schemas.ErrorResponse().model_dump())

    reservation_response = reservation_response.json()
    params = {'data': [reservation_response["paymentUid"]]}
    resp = await serviceRequests.get(url_payment_serv, params=params, headers={'Authorization': f"Bearer {token}"})

    payment = {}
    if resp is not None and resp.status_code == status.HTTP_200_OK:
        payment_response = resp.json()
        payment = schemas.PaymentInfo(
            status=payment_response[0]['status'],
            price=payment_response[0]['price']
        )
    else:
        print(resp.url)
        print(resp)
        if resp is not None and resp.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())

    return schemas.ReservationResponse(
        reservationUid=reservation_response['reservationUid'],
        hotel=reservation_response['hotel'],
        startDate=reservation_response['startDate'],
        endDate=reservation_response['endDate'],
        status=reservation_response['status'],
        payment=payment
    )


async def create_reservation(reservRequest: schemas.CreateReservationRequest, token: str):
    url_reserv_serv = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}{settings['prefix']}"
    url_payment_serv = f"http://{settings['payment_serv_host']}:{settings['payment_serv_port']}{settings['prefix']}"
    url_loyalty_serv = f"http://{settings['loyalty_serv_host']}:{settings['loyalty_serv_port']}{settings['prefix']}" \
                       f"/loyalty"
    header = {'Authorization': f"Bearer {token}"}
    resp = await serviceRequests.get(url_reserv_serv + f'/hotels/{reservRequest.hotelUid}', headers=header)

    if resp is None or resp.status_code != status.HTTP_200_OK:
        if resp is None or resp.status_code >= 500:
            return JSONResponse(status_code=503, content=schemas.UnavailableService(message="Reservation Service unavailable")
                            .model_dump())
        elif resp.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())
        raise RequestValidationError(errors=[{"field": "hotelUid",
                                              "msg": "invalid hotel uuid. no such hotel"}])

    hotel_resp = resp.json()
    cost = (reservRequest.endDate - reservRequest.startDate).days * hotel_resp['price']
    loyalty_info: schemas.LoyaltyInfoResponse = (await get_loyalty(token))

    if is_response(loyalty_info):
        if loyalty_info is not None and loyalty_info.status_code >= 500:
            return JSONResponse(status_code=503, content=schemas.UnavailableService(message="Loyalty Service unavailable")
                                .model_dump())
        elif loyalty_info.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())
        else:
            raise RequestValidationError(errors=[{"field": "username",
                                                  "msg": "client with such username does not exist"}])

    cost *= 0.01 * (100 - loyalty_info['discount'])
    cost = int(cost + 0.5)
    resp = await serviceRequests.post(url_payment_serv + f'/payments', headers={"X-Payment-Price": str(int(cost)), 'Authorization': f"Bearer {token}"})

    if resp is None or resp.status_code != status.HTTP_200_OK:
        print(cost)
        print(resp)
        if resp is not None and resp.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())
        elif resp is None or resp.status_code < 500:
            raise RequestValidationError(errors=[{"field": "payment_info",
                                                  "msg": "error in POST payment"}])
        return JSONResponse(status_code=503, content=schemas.UnavailableService(message="Payment Service unavailable")
                            .model_dump())

    pay_info = resp.json()
    resp = await serviceRequests.patch(url_loyalty_serv, headers=header, data=schemas.LoyaltyInfoRequest(
        reservationCountOperation=1
    ).model_dump(mode='json'))

    if resp is None or resp.status_code != status.HTTP_200_OK:
        serviceRequests.rollback(url_payment_serv + f'/payments/{pay_info["uid"]}', serviceRequests.requests.patch,
                                 headers=header,
                                 data=schemas.UpdatePaymentRequest(
                                           status='CANCELED'
                                       ).model_dump(mode='json'))
        if resp is not None and resp.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())
        elif resp is None or resp.status_code < 500:
            raise RequestValidationError(errors=[{"field": "loyalty",
                                                "msg": "error in PATCH method"}])
        return JSONResponse(status_code=503, content=schemas.UnavailableService(message="Loyalty Service unavailable")
                            .model_dump())

    resp = await serviceRequests.post(url_reserv_serv + f'/reservations', headers=header,
                                      data=schemas.CreateReservationRequestForReservService(
                                          paymentUid=pay_info['uid'],
                                          hotelUid=hotel_resp['hotelUid'],
                                          startDate=reservRequest.startDate,
                                          endDate=reservRequest.endDate
                                      ).model_dump(mode='json'))

    if resp is None or resp.status_code != status.HTTP_200_OK:
        print(schemas.CreateReservationRequestForReservService(
            paymentUid=pay_info['uid'],
            hotelUid=hotel_resp['hotelUid'],
            startDate=reservRequest.startDate,
            endDate=reservRequest.endDate
        ).model_dump(mode='json'))
        print(resp)

        serviceRequests.rollback(url_payment_serv + f'/payments/{pay_info["uid"]}', serviceRequests.requests.patch,
                                 headers=header,
                                 data=schemas.UpdatePaymentRequest(
                                           status='CANCELED'
                                       ).model_dump(mode='json'))
        serviceRequests.rollback(url_loyalty_serv, serviceRequests.requests.patch, headers=header,
                                 data=schemas.LoyaltyInfoRequest(
                                    reservationCountOperation=-1
                                 ).model_dump(mode='json'))
        if resp is not None and resp.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())
        elif resp is None or resp.status_code < 500:
            raise RequestValidationError(errors=[{"field": "reservation",
                                                  "msg": "error in POST reservation method"}])
        return JSONResponse(status_code=503, content=schemas.UnavailableService(message="Reservation Service unavailable")
                            .model_dump())

    reservResponse = resp.json()
    return schemas.CreateReservationResponse(
        reservationUid=reservResponse['reservationUid'],
        hotelUid=reservResponse['hotelUid'],
        startDate=reservResponse['startDate'],
        endDate=reservResponse['endDate'],
        discount=loyalty_info['discount'],
        status=reservResponse['status'],
        payment=schemas.PaymentInfo(
            status=pay_info['status'],
            price=pay_info['price']
        )
    )


async def delete_reservation(reservationUid: UUID, token: str):
    url_reserv_serv = f"http://{settings['reservation_serv_host']}:{settings['reservation_serv_port']}{settings['prefix']}"
    url_payment_serv = f"http://{settings['payment_serv_host']}:{settings['payment_serv_port']}{settings['prefix']}"
    url_loyalty_serv = f"http://{settings['loyalty_serv_host']}:{settings['loyalty_serv_port']}{settings['prefix']}" \
                       f"/loyalty"
    header = {'Authorization': f"Bearer {token}"}

    reservation = await get_reservation_by_uid(reservationUid, token)
    if not is_response(reservation) and reservation.status == "CANCELED":
        return status.HTTP_204_NO_CONTENT

    resp = await serviceRequests.patch(url_reserv_serv + f'/reservations/{reservationUid}', headers=header,
                                       data=schemas.UpdateReservationRequestForReservService(
                                           status='CANCELED'
                                       ).model_dump(mode='json'))

    if resp is None or resp.status_code != status.HTTP_200_OK:
        print("error in PATCH reservation method")
        print("headers:", header)
        print(schemas.UpdateReservationRequestForReservService(status='CANCELED').model_dump(mode='json'))
        print(resp)
        if resp is not None and resp.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())
        elif resp is not None and resp.status_code == status.HTTP_404_NOT_FOUND:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=schemas.ErrorResponse(message='Reservation not found').model_dump())
        else:
            return JSONResponse(status_code=503, content=schemas.UnavailableService(message="Reservation Service unavailable")
                                .model_dump())

    reserv_info_resp = resp.json()
    resp = await serviceRequests.patch(url_payment_serv + f'/payments/{reserv_info_resp["paymentUid"]}',
                                       headers=header,
                                       data=schemas.UpdatePaymentRequest(
                                           status='CANCELED'
                                       ).model_dump(mode='json'))

    if resp is None or resp.status_code != status.HTTP_200_OK:
        print("error in PATCH payment method")
        print(schemas.UpdatePaymentRequest(status='CANCELED').model_dump(mode='json'))
        print(resp)
        serviceRequests.rollback(url_reserv_serv + f'/reservations/{reservationUid}', serviceRequests.requests.patch,
                                 headers=header, data=schemas.UpdateReservationRequestForReservService(
                                                        status='PAID'
                                                      ).model_dump(mode='json'))
        if resp is not None and resp.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())
        else:
            return JSONResponse(status_code=503, content=schemas.UnavailableService(message="Payment Service unavailable")
                                .model_dump())

    resp = await serviceRequests.patch(url_loyalty_serv, headers=header, data=schemas.LoyaltyInfoRequest(
        reservationCountOperation=-1
    ).model_dump(mode='json'))

    if resp is None or resp.status_code != status.HTTP_200_OK:
        print("error in PATCH loyalty method")
        print("headers:", header)
        print(schemas.LoyaltyInfoRequest(reservationCountOperation=-1).model_dump(mode='json'))
        print(resp)
        if resp is not None and resp.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())
        serviceRequests.rollback(url_loyalty_serv, serviceRequests.requests.patch,  headers=header,
                                 data=schemas.LoyaltyInfoRequest(
                                    reservationCountOperation=-1
                                 ).model_dump(mode='json'))

    return status.HTTP_204_NO_CONTENT


async def get_loyalty(token: str):
    url_loyalty_serv = f"http://{settings['loyalty_serv_host']}:{settings['loyalty_serv_port']}{settings['prefix']}" \
                       f"/loyalty"
    response = await serviceRequests.get(url_loyalty_serv, headers={'Authorization': f"Bearer {token}"})

    if response is None or response.status_code != status.HTTP_200_OK:
        print("error in GET loyalty method")
        print(response)
        if response is not None and response.status_code >= 500:
            return JSONResponse(status_code=503, content=schemas.UnavailableService(message="Loyalty Service unavailable")
                                .model_dump())
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=schemas.ErrorResponse(message='Unauthorized').model_dump())
        else:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return response.json()


async def register_user(request: Request):
    url = f"http://{settings['identity_serv_host']}:{settings['identity_serv_port']}{settings['prefix']}/register"
    data = await request.json()
    res = (await serviceRequests.post(url=url, headers=request.headers, data=data, params=request.query_params))
    return JSONResponse(status_code=res.status_code, content=dict(res.json()))


async def auth_user(request: schemas.AuthenticationRequest):
    url = f"http://{settings['identity_serv_host']}:{settings['identity_serv_port']}{settings['prefix']}/oauth/token"
    res = (await serviceRequests.post(url=url, data=request.model_dump(mode='json')))
    return JSONResponse(status_code=res.status_code, content=dict(res.json()))


async def logout(request: Request):
    url = f"http://{settings['identity_serv_host']}:{settings['identity_serv_port']}{settings['prefix']}/oauth/revoke"
    return (await serviceRequests.post(url=url, headers=request.headers, params=request.query_params)).json()


async def get_statistic(token: str):
    url = f"http://{settings['statistic_serv_host']}:{settings['statistic_serv_port']}{settings['prefix']}/statistic/all"
    return (await serviceRequests.get(url=url, headers={"Authorization": token})).json()


async def get_service_avg(token: str):
    url = f"http://{settings['statistic_serv_host']}:{settings['statistic_serv_port']}{settings['prefix']}/statistic/services/avg-time"
    return (await serviceRequests.get(url=url, headers={"Authorization": token})).json()


async def get_query_avg(token: str):
    url = f"http://{settings['statistic_serv_host']}:{settings['statistic_serv_port']}{settings['prefix']}/statistic/queries/avg-time"
    return (await serviceRequests.get(url=url, headers={"Authorization": token})).json()
