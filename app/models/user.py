from sqlalchemy import Column, String
from sqlalchemy.sql.expression import false, text
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP, BigInteger

from ..config.database import Model


class User(Model):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email_verified_at = Column(TIMESTAMP(timezone=True), nullable=True)
    email_verification_token = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    UniqueConstraint(email)
