from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    university = Column(String)
    degree = Column(String)
    age = Column(Integer)
    gender = Column(String)
    job_role = Column(String)
    experience_years = Column(Integer)
    resume_filename = Column(String)