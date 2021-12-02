
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from ...models.user import User
from ...schema.user_schema import UserEmailToken
from ...config.database import config

EMAIL_TOKEN_SECRET_KEY = config['EMAIL_TOKEN_SECRET_KEY']
ACCESS_TOKEN_SECRET_KEY = config['ACCESS_TOKEN_SECRET_KEY']
ALGORITHM = config['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = config['ACCESS_TOKEN_EXPIRE_MINUTES']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

class UserOperations:
    def __init__(self, db):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_user(self, data):
        token_expiration = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        email_token = self.create_access_token(
            data = {
                "sub": data.email
            },
            secret_key = EMAIL_TOKEN_SECRET_KEY,
            expires_delta = token_expiration)

        user = User(**{
            "email": data.email,
            "password_hash": self.pwd_context.hash(data.password),
            "email_verification_token": email_token
        })

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_user(self, id):
        data = self.db.query(User).filter(User.id == id).first()
        return data

    def get_user_by_email(self, email):
        data = self.db.query(User).filter(User.email == email).first()
        return data

    def verify_user_email(self, token):
        token_data = UserOperations.verify_token(token, EMAIL_TOKEN_SECRET_KEY)

        user = self.get_user_by_email(email=token_data.email)
        if user is None:
            raise UserOperations.unauthorized_access()
        else:
            if user.email_verification_token == token:
                self.activate_user(user)
            else:
                raise UserOperations.unauthorized_access()
        return True

    def activate_user(self, user):
        user.email_verified_at = datetime.now()
        user.email_verification_token = None
        self.db.commit()

        return True

    def authenticate_user(self, form_data):
        user = self.get_user_by_email(email=form_data.username)
        if not user:
            raise UserOperations.forbidden_access()
        if not self.verify_password(form_data.password, user.password_hash):
            raise UserOperations.forbidden_access()
        return self.get_access_token(user)

    def get_access_token(self, user):
        if not user:
            raise UserOperations.forbidden_access()
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES) * 24)
        access_token = self.create_access_token(
            data = {
                "sub": user.email
            },
            secret_key = ACCESS_TOKEN_SECRET_KEY,
            expires_delta = access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}

    def verify_password(self, password_plain, password_hash):
        return self.pwd_context.verify(password_plain, password_hash)

    def create_access_token(self, data: dict, secret_key: str, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)

        return encoded_jwt

    @classmethod
    def verify_user_request(cls, token: str = Depends(oauth2_scheme)):
        return UserOperations.verify_token(token)

    @classmethod
    def verify_token(cls, token, secret_key = ACCESS_TOKEN_SECRET_KEY):
        try:
            payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise UserOperations.unauthorized_access()
            token_data = UserEmailToken(email=email)
        except JWTError:
            raise UserOperations.unauthorized_access()
        return token_data

    @classmethod
    def forbidden_access(cls):
        return HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Incorrect username or password",
            headers = { "WWW-Authenticate": "Bearer" },
        )

    @classmethod
    def unauthorized_access(cls):
        return HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid token!",
            headers = { "WWW-Authenticate": "Bearer" },
        )