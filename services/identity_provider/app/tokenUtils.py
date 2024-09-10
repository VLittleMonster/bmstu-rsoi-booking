from schemas.dto import UserInfo, TokenResponse
from schemas.ScopeTypes import ScopeTypes
import models
from pydantic import BaseModel
from sqlalchemy.orm import Session
import random
from jose import jwk, jws, jwt
from jose.utils import base64url_decode
from config import config
import time
import uuid
from fastapi import HTTPException
from validator import AlgTypes, TokenStandard, TokenTypes, LEEWAY
from okta_jwt_verifier.exceptions import JWTValidationException
from threading import Thread
from jwcrypto import jwk as jwk_gen

settings = config.get_settings()


class TokenMaster:
    __revoked_tokens_remover: Thread = None
    __key_generator: Thread = None

    class __Header(BaseModel):
        alg: str
        typ: str
        kid: str
        token_type: str

    class __AccessTokenPayload(BaseModel):
        jti: str
        username: str
        role: str
        first_name: str
        last_name: str
        patronymic: str
        phone_number: str
        email: str
        iss: str
        iat: int
        exp: int
        device_id: str

    class __RefreshTokenPayload(BaseModel):
        jti: str
        iss: str
        iat: int
        exp: int
        device_id: str

    @staticmethod
    def generate_signed_tokens(user: UserInfo, scope: str, db: Session) -> TokenResponse:
        if ScopeTypes.OPENID.value not in scope.lower():
            raise HTTPException(401, "Unauthorized")
        device_id = str(uuid.uuid4())
        access_token, exp_time = TokenMaster.__generate_signed_access_token(user, device_id, scope, db)
        refresh_token = TokenMaster.__generate_signed_refresh_token(user, device_id, db)
        return TokenResponse(access_token=access_token,
                             refresh_token=refresh_token,
                             scope=scope,                       # "openid profile email"
                             expires_in=exp_time,
                             token_type="Bearer")

    @staticmethod
    def __generate_signed_access_token(user: UserInfo, device_id: str, scope: str, db: Session) -> (str, int):
        key_list = TokenMaster.__get_jwks(db)
        key_dict = key_list[random.randint(0, len(key_list) - 1)].to_dict()
        exp_time = int(time.time()) + settings["access_token_exp_period_minutes"] * 60
        jwt_token = jws.sign(
            headers=TokenMaster.__Header(
                alg=key_dict['alg'],
                typ=TokenStandard.JWT.value,
                kid=key_dict['kid'],
                token_type=TokenTypes.ACCESS_TOKEN.value
            ).model_dump(),
            payload=TokenMaster.__AccessTokenPayload(
                jti=str(uuid.uuid4()),
                username=user.username,
                role=user.role,
                first_name=user.first_name if ScopeTypes.PROFILE.value in scope.lower() else "",
                last_name=user.last_name if ScopeTypes.PROFILE.value in scope.lower() else "",
                patronymic=user.patronymic if ScopeTypes.PROFILE.value in scope.lower() else "",
                phone_number=user.phone_number if ScopeTypes.PROFILE.value in scope.lower() else "",
                email=user.email if ScopeTypes.PROFILE.value in scope.lower() or ScopeTypes.EMAIL.value in scope.lower() else "",
                iss=settings["host_name"],
                iat=int(time.time()),
                exp=exp_time,
                device_id=device_id
            ).model_dump(),
            key=jwk.construct(key_dict),
            algorithm=key_dict["alg"]
        )

        return jwt_token, exp_time

    @staticmethod
    def __generate_signed_refresh_token(user: UserInfo, device_id: str, db: Session) -> str:
        TokenMaster.schedule_remove_revoked_tokens(db)

        key_list = TokenMaster.__get_jwks(db)
        key_dict = key_list[random.randint(0, len(key_list) - 1)].to_dict()
        payload = TokenMaster.__RefreshTokenPayload(
            jti=str(uuid.uuid4()),
            iss=settings["host_name"],
            iat=int(time.time()),
            exp=int(time.time()) + settings["refresh_token_exp_period_days"] * 24 * 3600,
            device_id=device_id
        ).model_dump()
        jwt_token = jws.sign(
            headers=TokenMaster.__Header(
                alg=key_dict['alg'],
                typ=TokenStandard.JWT.value,
                kid=key_dict['kid'],
                token_type=TokenTypes.REFRESH_TOKEN.value
            ).model_dump(),
            payload=payload,
            key=jwk.construct(key_dict),
            algorithm=key_dict["alg"]
        )

        issued_token = models.IssuedJWTToken(jti=payload['jti'], user_info=user,
                                             device_id=device_id, exp=payload["exp"], db=db)
        try:
            db.add(issued_token)
            db.commit()
            db.refresh(issued_token)
        except Exception as e:
            print(e)
            raise HTTPException(401, 'Unauthorized')
        return jwt_token

    @staticmethod
    def update_tokens(old_refresh_token: str, scope: str, db: Session) -> TokenResponse:
        claims = TokenMaster.__verify_refresh_token(old_refresh_token, db)
        try:
            TokenMaster.__revoke_token(claims=claims, db=db)
            revoked_token = db.query(models.IssuedJWTToken) \
                .filter(models.IssuedJWTToken._jti == claims['jti']).first()

            user = db.query(models.User).filter(models.User._id == revoked_token._subject).first()
            user = user.get_dto_model()
        except Exception as e:
            print(f"Token update error: {str(e)}")
            raise HTTPException(401, "Unauthorized")

        new_access_token, exp_time = TokenMaster.__generate_signed_access_token(user, claims["device_id"], scope=scope, db=db)
        new_refresh_token = TokenMaster.__generate_signed_refresh_token(user, claims["device_id"], db=db)
        return TokenResponse(
            refresh_token=new_refresh_token,
            access_token=new_access_token,
            scope=scope,                            # "openid profile phone"
            expires_in=exp_time,
            token_type="Bearer"
        )

    @staticmethod
    def revoke_token(refresh_token: str, db: Session):
        claims = TokenMaster.__verify_refresh_token(refresh_token, db)
        TokenMaster.__revoke_token(claims=claims, db=db)

    @staticmethod
    def __revoke_token(claims, db: Session):
        try:
            db.query(models.IssuedJWTToken) \
                .filter(models.IssuedJWTToken._jti == claims['jti']) \
                .update({"_revoked": True})
            db.commit()
        except Exception as e:
            print(f"Token revoke error: {str(e)}")
            raise HTTPException(401, "Unauthorized")

    @staticmethod
    def __verify_refresh_token(token, db: Session):
        try:
            header, claims, signing_input, signature = TokenMaster.__parse_token(token)
            TokenMaster.__verify_alg(header)
            TokenMaster.__verify_typ(header)
            TokenMaster.__verify_token_type(header)
            TokenMaster.__verify_iss(payload=claims)
            TokenMaster.__verify_expiration(payload=claims)

            jwk = TokenMaster.__get_jwk(header['kid'], db=db)
            TokenMaster.__verify_signature(token, signature, jwk)

            issued_token = db.query(models.IssuedJWTToken).filter(models.IssuedJWTToken._jti == claims['jti']).first()

            if issued_token._revoked:
                db.query(models.IssuedJWTToken).filter(models.IssuedJWTToken._subject == issued_token._subject) \
                    .filter(models.IssuedJWTToken._device_id == issued_token._device_id) \
                    .update({"_revoked": True})
                db.commit()
                raise JWTValidationException('Token was revoked!')
        except Exception as err:
            print(f"Verify error: {str(err)}")
            raise HTTPException(401, "Unauthorized")
        return claims

    @staticmethod
    def __parse_token(token):
        _, _, sign = token.split('.')
        header, payload = {}, {}
        try:
            header = jwt.get_unverified_header(token)
            payload = jwt.get_unverified_claims(token)
        except Exception as e:
            print(f"parsing token error: {str(e)}")
            raise JWTValidationException(f"parsing token error: {str(e)}")
        return header, payload, sign, base64url_decode(sign + '=' * (4 - len(sign) % 4))

    @staticmethod
    def __verify_signature(token, signature, jwk_key):
        key = jwk.construct({
            "kty": jwk_key['kty'],
            "alg": jwk_key['alg'],
            "use": jwk_key['use'],
            "e": jwk_key['e'],
            "n": jwk_key['n'],
            "kid": jwk_key['kid'],
        })
        try:
            header, payload, _ = token.split('.')
            if not key.verify(bytes(header + '.' + payload, 'UTF-8'), signature):
                raise JWTValidationException('Invalid token. Signature verifying error.')
        except Exception as e:
            raise JWTValidationException(f'verifying error: {e}')

    @staticmethod
    def __verify_alg(header):
        if header["alg"] != AlgTypes.RS256.value:
            print("Header claim \"alg\" is invalid")
            raise JWTValidationException("Header claim \"alg\" is invalid")

    @staticmethod
    def __verify_typ(header):
        if header["typ"] != TokenStandard.JWT.value:
            print("Invalid typ")
            raise JWTValidationException("Invalid typ")

    @staticmethod
    def __verify_token_type(header):
        if header["token_type"] != TokenTypes.REFRESH_TOKEN.value:
            print("Invalid token_type")
            raise JWTValidationException("Invalid token_type")

    @staticmethod
    def __verify_iss(payload):
        if payload["iss"] != settings["host_name"]:
            print("Invalid iss")
            raise JWTValidationException("Invalid iss")

    @staticmethod
    def __verify_expiration(payload, leeway=LEEWAY):
        exp = payload["exp"]
        now = int(time.time())
        if exp + leeway < now:
            print("exp: ", exp)
            print("now: ", now)
            print("Signature has expired")
            raise JWTValidationException("Signature has expired")

    @staticmethod
    def __get_jwks(db: Session):
        key_list = []
        try:
            key_list = list(db.query(models.JWK).all())
        except Exception as e:
            print(f'TokenUtils: error in getting jwks: {str(e)}')
            raise HTTPException(401, 'Unauthorized')
        if len(key_list) <= 0:
            print("Public keys list is empty!")
            raise HTTPException(401, 'Unauthorized')
        return key_list

    @staticmethod
    def __get_jwk(kid: str, db: Session):
        key = db.query(models.JWK).filter(models.JWK._kid == kid).first()
        key = key.to_dict()
        #print(key)
        return key

    @staticmethod
    def schedule_remove_revoked_tokens(db: Session):
        def schedule_removing():
            while True:
                remove_tokens()
                time.sleep(3600 * 24)

        def remove_tokens(leeway=LEEWAY):
            try:
                now = int(time.time()) - leeway
                db.query(models.IssuedJWTToken).filter(models.IssuedJWTToken._expired_in < now).delete()
                db.commit()
            except Exception as e:
                print(f"error in removing revoked tokens: {str(e)}")

        if TokenMaster.__revoked_tokens_remover is None:
            TokenMaster.__revoked_tokens_remover = Thread(target=schedule_removing)
            TokenMaster.__revoked_tokens_remover.start()

    @staticmethod
    def schedule_gen_keys(db: Session):
        #print("check keys")

        def gen_keys():
            try:
                db.query(models.JWK).delete()
                db.commit()
            except Exception as e:
                print(f'Try to clear keys: {str(e)}')

            for i in range(settings['num_of_keys']):
                new_key = models.JWK(key=jwk_gen.JWK.generate(
                    kty='RSA',
                    size=2048,
                    kid=str(uuid.uuid4()),
                    use='sig',
                    e=settings["key_exp"],
                    alg='RS256'
                ))

                try:
                    db.add(new_key)
                    db.commit()
                    db.refresh(new_key)
                except Exception as e:
                    print(f'Try to create keys: {str(e)}')

        keys = list(db.query(models.JWK).all())
        if len(keys) != settings['num_of_keys'] or keys[0]._exp < int(time.time()):
            gen_keys()
        """def schedule_gen():
            while True:
                JWKs = list(db.query(models.JWK).all())
                while len(JWKs) != settings['num_of_keys']:
                    gen_keys()
                    JWKs = list(db.query(models.JWK).all())
                now = int(time.time())
                exp_time = JWKs[0]._exp
                time.sleep(max(0, exp_time - now))

        if TokenMaster.__key_generator is None:
            TokenMaster.__key_generator = Thread(target=schedule_gen)
            TokenMaster.__key_generator.start()"""
