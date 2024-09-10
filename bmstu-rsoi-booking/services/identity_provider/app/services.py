from models import User, JWK as JWKey
from sqlalchemy.orm import Session
from schemas.dto import RegisterUserRequest, AuthenticationRequest, JWK, JWKsResponse, TokenResponse
from schemas.GrantTypes import GrantTypes
from config import config
from tokenUtils import TokenMaster
from fastapi.exceptions import HTTPException

settings = config.get_settings()


async def get_jwks(db: Session):
    TokenMaster.schedule_gen_keys(db)
    JWKs = list(db.query(JWKey).all())
    jwks = []
    for key in JWKs:
        jwks.append(key.model_dumps())
    return JWKsResponse(keys=jwks)


async def register_user(user_info: RegisterUserRequest, db: Session) -> TokenResponse:
    TokenMaster.schedule_gen_keys(db)
    if is_valid(user_info.username) and is_valid(user_info.password) and \
            is_valid(user_info.first_name) and  is_valid(user_info.last_name) and \
            is_valid(user_info.phone_number) and is_valid(user_info.email):
        patronymic = user_info.patronymic if user_info.patronymic else ""
        new_client = User(username=user_info.username,
                          password=user_info.password,
                          first_name=user_info.first_name,
                          last_name=user_info.last_name,
                          patronymic=patronymic,
                          phone_number=user_info.phone_number,
                          email=user_info.email)
    else:
        raise HTTPException(400, detail="Bad request")
    try:
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
    except Exception as e:
        print(e)
        if 'already exists' in str(e):
            raise HTTPException(200, detail="OK")
        raise HTTPException(500, detail="Internal server error")

    new_client = new_client.get_dto_model()
    return TokenMaster.generate_signed_tokens(new_client, user_info.scope, db)


async def auth_user(request: AuthenticationRequest, db: Session) -> TokenResponse:
    TokenMaster.schedule_gen_keys(db)
    if request.grant_type == GrantTypes.PASSWORD:
        user = db.query(User).filter(User._username == request.username).first()
        print("user: ", user)
        if user is None or not user.verify_password(request.password):
            raise HTTPException(401, detail="Unauthorized")
        return TokenMaster.generate_signed_tokens(user.get_dto_model(), request.scope, db)
    elif request.grant_type == GrantTypes.REFRESH_TOKEN:
        return TokenMaster.update_tokens(request.refresh_token, request.scope, db)
    raise HTTPException(status_code=401, detail="Unauthorized")


async def logout(refresh_token: str, db: Session) -> None:
    TokenMaster.schedule_gen_keys(db)
    TokenMaster.revoke_token(refresh_token, db)


def is_valid(field: str) -> bool:
    return field and len(field) > 0
