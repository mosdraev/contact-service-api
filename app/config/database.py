from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

config = {**dotenv_values(".env")}

SQLALCHEMY_DATABASE_URL = config['DB_DSN']

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Model = declarative_base()

def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()