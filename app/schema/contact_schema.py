from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from pydantic.networks import EmailStr


class ContactBase(BaseModel):
    id: Optional[int] = None
    owner_id: Optional[int] = None


class ContactForm(ContactBase):
    email: EmailStr
    firstname: str
    lastname: str


class ContactData(ContactForm):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Contacts(BaseModel):
    contacts: List[ContactData] = []
