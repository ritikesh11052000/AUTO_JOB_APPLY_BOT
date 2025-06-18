from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    profile_data: Optional[dict] = None
    preferences: Optional[dict] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class JobBase(BaseModel):
    title: str
    company: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    posted_date: Optional[datetime] = None
    source: Optional[str] = None
    url: Optional[str] = None

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int

    class Config:
        orm_mode = True

class ApplicationBase(BaseModel):
    resume_version: Optional[str] = None
    application_date: Optional[datetime] = None
    status: Optional[str] = None
    response_received: Optional[bool] = False

class ApplicationCreate(ApplicationBase):
    user_id: int
    job_id: int

class Application(ApplicationBase):
    id: int
    user_id: int
    job_id: int

    class Config:
        orm_mode = True
