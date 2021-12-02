from datetime import datetime, timedelta
from typing import Optional

from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from ...config.database import config
from ...routers.exception import Exception
from ...schema.user_schema import UserEmailToken

EMAIL_TOKEN_SECRET_KEY = config['EMAIL_TOKEN_SECRET_KEY']
ACCESS_TOKEN_SECRET_KEY = config['ACCESS_TOKEN_SECRET_KEY']
ALGORITHM = config['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = config['ACCESS_TOKEN_EXPIRE_MINUTES']


class OAuth2:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

    @classmethod
    def verify_user_request(cls, token: str = Depends(oauth2_scheme)):
        return OAuth2.verify_token(token)

    @classmethod
    def verify_token(cls, token, secret_key = ACCESS_TOKEN_SECRET_KEY):
        try:
            payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise Exception.unauthorized_access()
            token_data = UserEmailToken(email=email)
        except JWTError:
            raise Exception.unauthorized_access()
        return token_data

    @classmethod
    def create_access_token(cls, data: dict, secret_key: str, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes = 15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm = ALGORITHM)

        return encoded_jwt

    @classmethod
    def get_access_token(cls, user):
        if not user:
            raise Exception.forbidden_access()
        access_token_expires = timedelta(minutes = int(ACCESS_TOKEN_EXPIRE_MINUTES) * 24)
        access_token = OAuth2.create_access_token(
            data = {
                "sub": user.email
            },
            secret_key = ACCESS_TOKEN_SECRET_KEY,
            expires_delta = access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
