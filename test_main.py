import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models

client = TestClient(app)

# Setup and teardown the database for tests
@pytest.fixture(scope="module")
def test_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(test_db: Session):
    response = client.post("/users/", json={
        "email": "testuser@example.com",
        "profile_data": {"skills": ["python", "fastapi"]},
        "preferences": {"location": "remote"}
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data

def test_get_user(test_db: Session):
    # Create user first
    response = client.post("/users/", json={
        "email": "getuser@example.com",
        "profile_data": {"skills": ["sqlalchemy"]},
        "preferences": {"location": "NY"}
    })
    user_id = response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "getuser@example.com"

def test_create_job(test_db: Session):
    response = client.post("/jobs/", json={
        "title": "Software Engineer",
        "company": "Tech Corp",
        "description": "Develop software",
        "requirements": "Python, FastAPI",
        "location": "Remote",
        "salary_range": "100000-120000",
        "source": "LinkedIn",
        "url": "http://example.com/job/1"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Software Engineer"
    assert "id" in data

def test_list_jobs(test_db: Session):
    response = client.get("/jobs/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_application(test_db: Session):
    # Create user and job first
    user_resp = client.post("/users/", json={"email": "applicant@example.com"})
    job_resp = client.post("/jobs/", json={"title": "DevOps Engineer"})
    user_id = user_resp.json()["id"]
    job_id = job_resp.json()["id"]
    response = client.post("/applications/", json={
        "user_id": user_id,
        "job_id": job_id,
        "resume_version": "v1",
        "status": "applied"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["job_id"] == job_id

def test_list_applications_for_user(test_db: Session):
    user_resp = client.post("/users/", json={"email": "listapp@example.com"})
    user_id = user_resp.json()["id"]
    response = client.get(f"/users/{user_id}/applications/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
