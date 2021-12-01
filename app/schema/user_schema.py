from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserData(BaseModel):
    id: Optional[int]
    email: EmailStr
    email_verified_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserRegister(UserData):
    password: str

class UserEmailToken(BaseModel):
    email: Optional[EmailStr] = None

class UserToken(BaseModel):
    access_token: str
    token_type: str
