from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..config.database import db
from ..models.operations.contact_operations import ContactOperations
from ..models.operations.oauth2 import OAuth2
from ..routers.app_exception import AppException
from ..schema.contact_schema import ContactData, ContactForm, Contacts

router = APIRouter(
    prefix='/contact',
    tags=['Contact']
)


# Get All Contacts of the current authenticated user
@router.get('s', response_model=Contacts)
def get_contacts(database: Session = Depends(db), current_user: str = Depends(OAuth2.verify_user_request)):
    operation = ContactOperations(database)
    contacts = operation.get_contacts(current_user.id)

    return contacts


# Get a single contact of the current authenticated user
@router.get('/{contact_id}', response_model=ContactData)
def get_contact(contact_id: int, database: Session = Depends(db),
                current_user: str = Depends(OAuth2.verify_user_request)):
    operation = ContactOperations(database)
    contact = operation.get_contact(current_user.id, contact_id)

    if not contact:
        raise AppException.resource_not_found("Contact does not exists.")

    return contact


# Create a contact of the current authenticated user
@router.post('', response_model=ContactData)
def add_contact(data: ContactForm, database: Session = Depends(db),
                current_user: str = Depends(OAuth2.verify_user_request)):
    operation = ContactOperations(database)
    new_contact = operation.create_contact(data, current_user.id)

    if new_contact is False:
        raise AppException.bad_request("Contact already exists.")

    return new_contact


# Update a contact of the current authenticated user
@router.put('/{contact_id}', response_model=ContactData)
def update_contact(contact_id: int, data: ContactForm, database: Session = Depends(db),
                   current_user: str = Depends(OAuth2.verify_user_request)):
    operation = ContactOperations(database)
    updated_contact = operation.update_contact(data, contact_id, current_user.id)

    if not updated_contact:
        raise AppException.resource_not_found("Contact does not exists.")

    return updated_contact


# Delete a contact of the current authenticated user
@router.delete('/{contact_id}')
def delete_contact(contact_id: int, database: Session = Depends(db),
                   current_user: str = Depends(OAuth2.verify_user_request)):
    operation = ContactOperations(database)
    status_result = operation.delete_contact(contact_id, current_user.id)

    if not status_result:
        raise AppException.resource_not_found("Contact no longer exists.")

    return status_result
