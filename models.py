from sqlite3 import Date
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from database import Base

class Student(Base):
    __tablename__ = 'books'

    surname = Column(String, index=True)
    lastname = Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    is_published = Column(Boolean, index=True)

