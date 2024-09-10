from pydantic import BaseModel
from typing import List


class JWK(BaseModel):
    kty: str
    use: str
    n: str
    e: str
    kid: str
    alg: str


class JWKsResponse(BaseModel):
    keys: List[JWK]


class UserInfo(BaseModel):
    username: str
    role: str
    first_name: str
    last_name: str
    patronymic: str
    phone_number: str
    email: str


class RegisterUserRequest(BaseModel):
    scope: str
    username: str
    password: str
    first_name: str
    last_name: str
    patronymic: str
    phone_number: str
    email: str


class TokenResponse(BaseModel):
    refresh_token: str
    access_token: str
    scope: str
    expires_in: int
    token_type: str


class AuthenticationRequest(BaseModel):
    scope: str
    grant_type: str
    username: str | None = None
    password: str | None = None
    refresh_token: str | None = None


class EventInfoMsg(BaseModel):
    eventUuid: str | None = None
    username: str
    eventAction: str
    startTime: float
    endTime: float
    serviceName: str
