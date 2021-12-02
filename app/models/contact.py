from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP, BigInteger, Integer

from ..config.database import Model


class Contact(Model):
    __tablename__ = "contacts"

    id = Column(BigInteger, primary_key=True, index=True)
    owner_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    type_id = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


    owner = relationship('User', back_populates='contacts')
    UniqueConstraint(email)
