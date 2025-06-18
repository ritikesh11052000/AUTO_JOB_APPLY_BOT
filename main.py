import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, database
import models
import schemas
import crud
from typing import List
from fastapi import Query
from job_search import JobSearch
from walkin_detection import filter_walkin_jobs
from resume_optimization import optimize_resume_for_job
from fastapi import Body
from pdf_generation import generate_pdf_resume

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auto Job Application Chatbot Backend")

job_searcher = JobSearch()

# Job search endpoint
@app.get("/search_jobs/", response_model=List[schemas.Job])
def search_jobs(query: str = Query(..., min_length=1), location: str = Query("", min_length=0)):
    jobs = job_searcher.search_jobs(query, location)
    return jobs

# Walk-in interview jobs endpoint
@app.get("/walkin_jobs/", response_model=List[schemas.Job])
def get_walkin_jobs(query: str = Query(..., min_length=1), location: str = Query("", min_length=0)):
    all_jobs = job_searcher.search_jobs(query, location)
    walkin_jobs = filter_walkin_jobs(all_jobs)
    return walkin_jobs

# ATS resume optimization endpoint
@app.post("/optimize_resume/", response_model=dict)
def optimize_resume(base_resume: dict = Body(...), job_description: str = Body(...)):
    optimized = optimize_resume_for_job(base_resume, job_description)
    return optimized

# PDF generation endpoint
@app.post("/generate_pdf/")
def generate_pdf(base_resume: dict = Body(...), company_name: str = Body(...), job_title: str = Body(...)):
    filepath = generate_pdf_resume(base_resume, company_name, job_title)
    return {"pdf_path": filepath}

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": "Welcome to the Auto Job Application Chatbot API"}

# User endpoints
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Job endpoints
@app.post("/jobs/", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db=db, job=job)

@app.get("/jobs/", response_model=List[schemas.Job])
def list_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = crud.list_jobs(db, skip=skip, limit=limit)
    return jobs

@app.get("/jobs/{job_id}", response_model=schemas.Job)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

# Application endpoints
@app.post("/applications/", response_model=schemas.Application)
def create_application(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(db=db, application=application)

@app.get("/users/{user_id}/applications/", response_model=List[schemas.Application])
def list_applications_for_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_applications_for_user(db, user_id=user_id, skip=skip, limit=limit)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
