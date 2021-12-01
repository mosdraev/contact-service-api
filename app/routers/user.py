from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..config.database import db
from ..models.operations.user_operations import UserOperations
from ..schema.user_schema import UserToken, UserData, UserRegister

router = APIRouter(
    prefix='/user',
    tags=['User']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Register a user
@router.post('/register', response_model = UserData)
def register_user(data: UserRegister, db: Session = Depends(db)):
    operation = UserOperations(db)
    status = operation.create_user(data)

    return status

# Verify & Activate a user
@router.get('/verify-email')
def verify_user_email(token: str, db: Session = Depends(db)):
    operation = UserOperations(db)
    status_result = operation.verify_user_email(token)

    if status_result == False:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Error {status.HTTP_404_NOT_FOUND}: Page not found.")
    return status_result

@router.post('/login', response_model = UserToken)
def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db)):
    operation = UserOperations(db)
    status_result = operation.authenticate_user(form_data)

    return status_result

# Get a user by id
@router.get("/{id}", response_model = UserData)
def get_user(id: int, db: Session = Depends(db), vemail: str = Depends(UserOperations.verify_user_request)):
    operation = UserOperations(db)
    status = operation.get_user(id)

    return status
