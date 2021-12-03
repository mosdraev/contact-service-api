from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..config.database import db
from ..models.operations.oauth2 import OAuth2
from ..models.operations.user_operations import UserOperations
from ..routers.app_exception import AppException
from ..schema.user_schema import UserData, UserRegister, UserToken

router = APIRouter(
    prefix='/user',
    tags=['User']
)


# Register a user
@router.post('/register', response_model=UserData)
def register_user(data: UserRegister, database: Session = Depends(db)):
    operation = UserOperations(database)
    status_result = operation.create_user(data)

    return status_result


# Verify & Activate a user
@router.get('/verify-email')
def verify_user_email(token: str, database: Session = Depends(db)):
    operation = UserOperations(database)
    status_result = operation.verify_user_email(token)

    if not status_result:
        raise AppException.resource_not_found(f"Error {status.HTTP_404_NOT_FOUND}: Page not found.")
    return status_result


# Authenticate a user
@router.post('/login', response_model=UserToken)
def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(db)):
    operation = UserOperations(database)
    status_result = operation.authenticate_user(form_data)

    return status_result


# Get a user by id
@router.get("/", response_model=UserData)
def get_user(database: Session = Depends(db), current_user: int = Depends(OAuth2.verify_user_request)):
    operation = UserOperations(database)
    status_result = operation.get_user(current_user.id)

    if not status_result:
        raise AppException.resource_not_found("User does not exists.")

    return status_result
