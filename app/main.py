from fastapi import FastAPI

from .config.database import engine
from .models.contact import Contact
from .models.profile import Profile
from .models.user import User
from .routers import contact, user

# TEMPORARY AUTOMATIC MIGRATIONS
User.metadata.create_all(bind=engine)
Profile.metadata.create_all(bind=engine)
Contact.metadata.create_all(bind=engine)

# Initialize FastAPI module
contact_service = FastAPI()
contact_service.include_router(user.router)
contact_service.include_router(contact.router)
