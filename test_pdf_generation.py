import os
import pytest
from pdf_generation import generate_pdf_resume

def test_generate_pdf_resume():
    resume_data = {
        "summary": "Experienced Python developer.",
        "skills": ["Python", "FastAPI", "SQL"],
        "experience": [
            {"title": "Software Engineer", "description": "Developed APIs using FastAPI."},
            {"title": "Backend Developer", "description": "Worked with PostgreSQL and Celery."}
        ],
        "education": ["BSc Computer Science"]
    }
    company_name = "TestCompany"
    job_title = "Backend Developer"

    pdf_path = generate_pdf_resume(resume_data, company_name, job_title)
    assert os.path.exists(pdf_path)
    assert pdf_path.endswith(".pdf")

    # Clean up generated file
    os.remove(pdf_path)
