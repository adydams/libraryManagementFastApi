from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String)
    created_at = Column(TIMESTAMP(timezone =True), nullable=False, server_default= text('now()'))

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published = Column(Boolean, default = True)
    ISBN = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone =True), nullable=False, server_default= text('now()'))

    createdby_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    createdby = relationship("User")

class Comment(Base):
    __tablename__ = "comments"

    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, primary_key=True,)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True,)
    comment = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone =True), nullable=False, server_default= text('now()'))
