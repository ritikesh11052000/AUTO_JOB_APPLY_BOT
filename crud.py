from sqlalchemy.orm import Session
from models import User, Job, Application
from schemas import UserCreate, JobCreate, ApplicationCreate
from datetime import datetime

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        profile_data=user.profile_data,
        preferences=user.preferences,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Job CRUD
def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()

def create_job(db: Session, job: JobCreate):
    db_job = Job(
        title=job.title,
        company=job.company,
        description=job.description,
        requirements=job.requirements,
        location=job.location,
        salary_range=job.salary_range,
        posted_date=job.posted_date,
        source=job.source,
        url=job.url
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def list_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Job).offset(skip).limit(limit).all()

# Application CRUD
def get_application(db: Session, application_id: int):
    return db.query(Application).filter(Application.id == application_id).first()

def create_application(db: Session, application: ApplicationCreate):
    db_application = Application(
        user_id=application.user_id,
        job_id=application.job_id,
        resume_version=application.resume_version,
        application_date=application.application_date or datetime.utcnow(),
        status=application.status,
        response_received=application.response_received
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def list_applications_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Application).filter(Application.user_id == user_id).offset(skip).limit(limit).all()
