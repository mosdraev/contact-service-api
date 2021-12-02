from datetime import datetime, timedelta

from passlib.context import CryptContext

from ...models.user import User
from ...routers.exception import Exception
from ..operations.oauth2 import (ACCESS_TOKEN_EXPIRE_MINUTES,
                                 EMAIL_TOKEN_SECRET_KEY, OAuth2)

class UserOperations:
    def __init__(self, db):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_user(self, data):
        token_expiration = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        email_token = OAuth2.create_access_token(
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
        token_data = OAuth2.verify_token(token, EMAIL_TOKEN_SECRET_KEY)

        user = self.get_user_by_email(email=token_data.email)
        if user is None:
            raise Exception.unauthorized_access()
        else:
            if user.email_verification_token == token:
                self.activate_user(user)
            else:
                raise Exception.unauthorized_access()
        return True

    def activate_user(self, user):
        user.email_verified_at = datetime.now()
        user.email_verification_token = None
        self.db.commit()

        return True

    def authenticate_user(self, form_data):
        user = self.get_user_by_email(email=form_data.username)
        if not user:
            raise Exception.forbidden_access()
        if not self.verify_password(form_data.password, user.password_hash):
            raise Exception.forbidden_access()
        return OAuth2.get_access_token(user)

    def verify_password(self, password_plain, password_hash):
        return self.pwd_context.verify(password_plain, password_hash)
