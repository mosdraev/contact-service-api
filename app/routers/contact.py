from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..config.database import db
from ..models.operations.contact_operations import ContactOperations
from ..models.operations.oauth2 import OAuth2
from ..routers.exception import Exception
from ..schema.contact_schema import ContactData, ContactForm, Contacts

router = APIRouter(
    prefix='/contact',
    tags=['Contact']
)

# Get All Contacts of the current authenticated user
@router.get('s', response_model = Contacts)
def get_contacts(db: Session = Depends(db), current_user: str = Depends(OAuth2.verify_user_request)):
    operation = ContactOperations(db)
    contacts = operation.get_contacts(current_user.id)

    return contacts

# Get a single contact of the current authenticated user
@router.get('/{id}', response_model = ContactData)
def get_contact(id: int, db: Session = Depends(db), current_user: str = Depends(OAuth2.verify_user_request)):
    operation = ContactOperations(db)
    contact = operation.get_contact(current_user.id, id)

    if not contact:
        raise Exception.resource_not_found("Contact does not exists.")

    return contact

# Create a contact of the current authenticated user
@router.post('', response_model = ContactData)
def add_contact(data: ContactForm, db: Session = Depends(db), current_user: str = Depends(OAuth2.verify_user_request)):
    operation = ContactOperations(db)
    new_contact = operation.create_contact(data, current_user.id)

    return new_contact

# Update a contact of the current authenticated user
@router.put('/{id}', response_model = ContactData)
def update_contact(id: int, data: ContactForm, db: Session = Depends(db), current_user: str = Depends(OAuth2.verify_user_request)):
    operation = ContactOperations(db)
    updated_contact = operation.update_contact(data, id, current_user.id)

    if not updated_contact:
        raise Exception.resource_not_found("Contact does not exists.")

    return updated_contact

# Delete a contact of the current authenticated user
@router.delete('/{id}')
def delete_contact(id: int, db: Session = Depends(db), current_user: str = Depends(OAuth2.verify_user_request)):
    operation = ContactOperations(db)
    status_result = operation.delete_contact(id, current_user.id)

    if not status_result:
        raise Exception.resource_not_found("Contact no longer exists.")

    return status_result

@router.post('/register/{form_id}')
def register_contact(form_id: str, db: Session = Depends(db)):
    pass
