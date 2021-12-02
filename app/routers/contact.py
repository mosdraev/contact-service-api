from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..models.operations.contact_operations import ContactOperations

from ..config.database import db
from ..models.operations.user_operations import UserOperations
from ..schema.contact_schema import ContactData, Contacts, ContactForm
from ..schema.user_schema import UserContacts

router = APIRouter(
    prefix='/contact',
    tags=['Contact']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


@router.get('/all-contacts/{owner_id}', response_model = Contacts)
def get_contacts(owner_id: int, db: Session = Depends(db), current_user: str = Depends(UserOperations.verify_user_request)):
    operation = ContactOperations(db)
    contacts = operation.get_contacts(owner_id)

    return contacts

@router.get('/{contact_id}', response_model = ContactData)
def get_contact(contact_id: int, db: Session = Depends(db), current_user: str = Depends(UserOperations.verify_user_request)):
    operation = ContactOperations(db)
    contact = operation.get_contact(contact_id)

    if not contact:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Contact does not exists."
        )

    return contact

@router.post('/{owner_id}', response_model = ContactData)
def add_contact(owner_id: int, data: ContactForm, db: Session = Depends(db), current_user: str = Depends(UserOperations.verify_user_request)):
    operation = ContactOperations(db)
    new_contact = operation.create_contact(data, owner_id)

    return new_contact

@router.put('/{contact_id}', response_model = ContactData)
def update_contact(contact_id: int, data: ContactForm, db: Session = Depends(db), current_user: str = Depends(UserOperations.verify_user_request)):
    operation = ContactOperations(db)
    updated_contact = operation.update_contact(data, contact_id)

    if not updated_contact:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Contact does not exists."
        )

    return updated_contact

@router.delete('/{contact_id}')
def delete_contact(contact_id: int, db: Session = Depends(db), current_user: str = Depends(UserOperations.verify_user_request)):
    operation = ContactOperations(db)
    status_result = operation.delete_contact(contact_id)

    if not status_result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Contact no longer exists."
        )

    return status_result

@router.post('/register/{form_id}')
def register_contact(form_id: str, db: Session = Depends(db)):
    pass