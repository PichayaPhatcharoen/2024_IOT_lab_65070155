from sqlite3 import Date
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
# from sqlalchemy.orm import relationship

from database import Base

class Student(Base):
    __tablename__ = 'students'

    surname = Column(String, index=True)
    lastname = Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)
    birthdate = Column(Date, index=True)
    gender = Column(String, index=True)

