from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    profile_data = Column(JSONB)
    preferences = Column(JSONB)
    created_at = Column(TIMESTAMP)

    applications = relationship("Application", back_populates="user")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    company = Column(String(255))
    description = Column(Text)
    requirements = Column(Text)
    location = Column(String(255))
    salary_range = Column(String(100))
    posted_date = Column(TIMESTAMP)
    source = Column(String(50))
    url = Column(String(500))

    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    resume_version = Column(String(255))
    application_date = Column(TIMESTAMP)
    status = Column(String(50))
    response_received = Column(Boolean, default=False)

    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
