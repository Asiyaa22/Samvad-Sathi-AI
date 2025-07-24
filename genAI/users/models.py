from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255), nullable=True)
    degree = Column(String(50), nullable=True)
    university = Column(String(100), nullable=True)
    date_of_birth = Column(String(20), nullable=True)
    #created at updated at
