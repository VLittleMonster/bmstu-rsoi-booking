import hashlib
import os
import time
from typing import Final

import jwcrypto.jwk as crypto_jwk
from sqlalchemy import Integer, Column, VARCHAR, DateTime, BOOLEAN, ForeignKey
from sqlalchemy.orm import Session

from config import config
from database.database import Base
from schemas.dto import JWK as JWK_dto
from schemas.dto import UserInfo

ROLES: Final = ['user', 'admin']
settings = config.get_settings()


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {
        'extend_existing': True
    }

    _id = Column(Integer, primary_key=True, name='id')
    _username = Column(VARCHAR(80), nullable=False, unique=True, name='username')
    __password_hash = Column(VARCHAR(), nullable=False, name='password_hash')
    __role = Column(VARCHAR(80), nullable=False, default=ROLES[0], name='role')
    __first_name = Column(VARCHAR(80), nullable=False, name='first_name')
    __last_name = Column(VARCHAR(80), nullable=False, name='last_name')
    __patronymic = Column(VARCHAR(80), name='patronymic')
    __phone_number = Column(VARCHAR(15), nullable=False, name='phone_number')
    __email = Column(VARCHAR(30), nullable=False, name='email')

    def __init__(self, username: str, password: str, first_name: str, last_name: str, patronymic: str,
                 phone_number: str, email: str):
        self._username = username
        self.__password_hash = self.__gen_password_hash(password)
        self.__first_name = first_name
        self.__last_name = last_name
        self.__patronymic = patronymic
        self.__phone_number = phone_number
        self.__email = email

    @staticmethod
    def __gen_password_hash(password: str, salt: bytes = os.urandom(16)) -> str:
        password_hash = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=password.encode('utf-8'),
            salt=salt,
            iterations=100000
        )
        return str(password_hash.hex()) + '.' + str(salt.hex())

    def verify_password(self, password: str) -> bool:
        _, salt = self.__password_hash.split('.')
        print("hash from db: ", self.__password_hash)
        print("got pass hash: ", self.__gen_password_hash(password=password, salt=bytes.fromhex(salt)))
        res = self.__password_hash == self.__gen_password_hash(password=password, salt=bytes.fromhex(salt))
        print("password verified? ", res)
        return res

    def get_dto_model(self):
        return UserInfo(
            username=self._username,
            role=self.__role,
            first_name=self.__first_name,
            last_name=self.__last_name,
            patronymic=self.__patronymic,
            phone_number=self.__phone_number,
            email=self.__email
        )


class JWK(Base):
    __tablename__ = 'jwks'
    __table_args__ = {
        'extend_existing': True
    }

    __id = Column(Integer, primary_key=True, name='id')
    _kid = Column(VARCHAR(100), nullable=False, unique=True, name='kid')
    __kty = Column(VARCHAR(10), nullable=False, default='RSA', name='kty')
    __use = Column(VARCHAR(10), nullable=False, default='sig', name='use')
    __n = Column(VARCHAR(4096), nullable=False, name='n')
    __d = Column(VARCHAR(4096), nullable=False, name='d')
    __e = Column(VARCHAR(4096), nullable=False, name='e')
    __alg = Column(VARCHAR(10), nullable=False, default='RS256', name='alg')
    _exp = Column(Integer, nullable=False, default=int(time.time()) + settings['keys_period_update']*24*3600, name='exp')

    def __init__(self, key: crypto_jwk.JWK):
        self._kid = key['kid']
        self.__n = key['n']
        self.__d = key['d']
        self.__e = key['e']

    def exp(self):
        return self._exp

    def model_dumps(self):
        return JWK_dto(
            kty=self.__kty,
            use=self.__use,
            n=self.__n,
            e=self.__e,
            kid=self._kid,
            alg=self.__alg
        )

    def to_dict(self) -> dict:
        key = {
            'kid': self._kid,
            'kty': self.__kty,
            'use': self.__use,
            'n': self.__n,
            'd': self.__d,
            'e': self.__e,
            'alg': self.__alg,
        }
        """print(self._kid)
        print(key["n"])
        print(key["e"])
        print(key["d"])
        print('='*10)"""
        return key


class IssuedJWTToken(Base):
    __tablename__ = 'issuedJWTTokens'
    __table_args__ = {
        'extend_existing': True
    }

    _jti = Column(VARCHAR(36), primary_key=True, name='jti')
    _subject = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, name='subject')
    _device_id = Column(VARCHAR(36), nullable=False, name='device_id')
    _revoked = Column(BOOLEAN, default=False, name='revoked')
    _expired_in = Column(Integer, nullable=False, name="expired_in")

    def __init__(self, jti: str, user_info: UserInfo, device_id: str, exp: int, db: Session):
        user = db.query(User).filter(User._username == user_info.username).one()
        self._jti = jti
        self._subject = user._id
        self._device_id = device_id
        self._expired_in = exp
