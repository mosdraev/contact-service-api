from fastapi import FastAPI
from .models.user import User
from .models.profile import Profile
from .config.database import engine
from .routers import user

# TEMPORARY AUTOMATIC MIGRATIONS
User.metadata.create_all(bind=engine)
Profile.metadata.create_all(bind=engine)

# Initialize FastAPI module
contact_service = FastAPI()
contact_service.include_router(user.router)
