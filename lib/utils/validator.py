import warnings

from urllib.parse import urljoin

from okta_jwt_verifier import __version__ as version
#from okta_jwt_verifier.constants import MAX_RETRIES, MAX_REQUESTS, REQUEST_TIMEOUT, LEEWAY
from okta_jwt_verifier.exceptions import JWKException, JWTValidationException
from okta_jwt_verifier.jwt_utils import JWTUtils

import base64, json, asyncio
import serviceRequests
from jose import jwk, jwt
from jose.utils import base64url_decode

from enum import Enum, unique
import time


@unique
class AlgTypes(Enum):
    RS256 = "RS256"


@unique
class TokenStandard(Enum):
    JWT = "JWT"


@unique
class TokenTypes(Enum):
    ACCESS_TOKEN = "access-token"
    REFRESH_TOKEN = "refresh-token"


ISSUER_IRL = 'http://identity-provider:8090/'
LEEWAY = 120    # секунд


class BaseJWTVerifier:
    def __init__(self,
                 issuer=None,
                 leeway=LEEWAY,
                 cache_jwks=True,
                 requests_cache={}):
        self.issuer = issuer
        self.cache_jwks = cache_jwks
        self.requests_cache = requests_cache
        self.leeway = leeway

    @staticmethod
    def parse_token(token):
        _, _, sign = token.split('.')
        header = jwt.get_unverified_header(token)
        payload = jwt.get_unverified_claims(token)
        print(header)
        print(payload)
        return header, payload, sign, base64url_decode(sign + '=' * (4 - len(sign) % 4))

    async def verify_access_token(self, token):
        try:
            header, claims, signing_input, signature = self.parse_token(token)
            self.__verify_alg(header)
            self.__verify_typ(header)
            self.__verify_token_type(header)
            self.__verify_iss(payload=claims)
            self.__verify_expiration(payload=claims)

            jwk = await self.get_jwk(header['kid'])
            self.verify_signature(token, signature, jwk)
        except JWTValidationException:
            raise
        except Exception as err:
            raise JWTValidationException(str(err))
        return claims

    @staticmethod
    def verify_signature(token, signature, jwk_key):
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
            raise JWTValidationException("Header claim \"alg\" is invalid")

    @staticmethod
    def __verify_typ(header):
        if header["typ"] != TokenStandard.JWT.value:
            raise JWTValidationException("Invalid typ")

    @staticmethod
    def __verify_token_type(header):
        if header["token_type"] != TokenTypes.ACCESS_TOKEN.value:
            raise JWTValidationException("Invalid token_type")

    @staticmethod
    def __verify_iss(payload):
        if payload["iss"] != ISSUER_IRL:
            raise JWTValidationException("Invalid iss")

    def __verify_expiration(self, payload):
        exp = payload["exp"]
        now = int(time.time())
        print("exp: ", exp)
        print("now: ", now)
        if exp + self.leeway < now:
            raise JWTValidationException("Signature has expired")
        #JWTUtils.verify_expiration(token, leeway)

    def _get_jwk_by_kid(self, jwks, kid):
        jwk_key = None
        for key in jwks['keys']:
            if key['kid'] == kid:
                jwk_key = key
        return jwk_key

    async def get_jwk(self, kid):
        jwks = await self.get_jwks()
        jwk_key = self._get_jwk_by_kid(jwks, kid)
        #print(jwks)

        if not jwk_key:
            # retry logic
            self._clear_requests_cache()
            jwks = await self.get_jwks()
            jwk_key = self._get_jwk_by_kid(jwks, kid)
        if not jwk_key:
            raise JWKException('No matching JWK.')
        return jwk_key

    async def get_jwks(self):
        if self.requests_cache is not None and len(self.requests_cache) > 0:
            return self.requests_cache
        jwks_uri = self._construct_jwks_uri()
        headers = {'User-Agent': f'jwt-verifier-python/{version}',
                   'Content-Type': 'application/json'}
        jwks = await serviceRequests.get(jwks_uri, headers=headers)
        jwks = jwks.json()
        if self.cache_jwks:
            self.requests_cache.update(jwks)
        return jwks

    def _construct_jwks_uri(self):
        jwks_uri_base = self.issuer
        if not jwks_uri_base.endswith('/'):
            jwks_uri_base = jwks_uri_base + '/'
        if '/.well-known/jwks.json' not in jwks_uri_base:
            jwks_uri_base = urljoin(jwks_uri_base, '.well-known/jwks.json')
        return jwks_uri_base

    def _clear_requests_cache(self):
        self.requests_cache.clear()


class Validator:

    @staticmethod
    async def validate_token(token, leeway=LEEWAY):
        try:
            print("got token: ", token)
            jwt_verifier = BaseJWTVerifier(issuer=ISSUER_IRL,
                                           leeway=leeway)  # user_info['iss'],
            payload = await jwt_verifier.verify_access_token(token)
            return payload
        except Exception as e:
            print(f"Validation error: {e}")
            return None

    @staticmethod
    async def get_userinfo(token):
        return await Validator.validate_token(token)
