import pytest
from resume_optimization import (
    extract_job_requirements,
    optimize_summary,
    prioritize_relevant_skills,
    highlight_relevant_experience,
    optimize_resume_for_job
)

def test_extract_job_requirements():
    job_desc = "Looking for Python developer with experience in FastAPI and SQL."
    keywords = extract_job_requirements(job_desc)
    assert "python" in keywords
    assert "fastapi" in keywords
    assert "sql" in keywords

def test_optimize_summary():
    base_summary = "Experienced developer."
    key_reqs = ["python", "fastapi"]
    optimized = optimize_summary(base_summary, key_reqs)
    assert "python" in optimized.lower()
    assert "fastapi" in optimized.lower()

def test_prioritize_relevant_skills():
    base_skills = ["Python", "Java", "FastAPI", "Docker"]
    key_reqs = ["python", "fastapi"]
    prioritized = prioritize_relevant_skills(base_skills, key_reqs)
    assert prioritized[0].lower() == "python"
    assert prioritized[1].lower() == "fastapi"

def test_highlight_relevant_experience():
    base_exp = [
        {"description": "Developed Python applications."},
        {"description": "Managed teams."}
    ]
    key_reqs = ["python"]
    highlighted = highlight_relevant_experience(base_exp, key_reqs)
    assert highlighted[0].get("highlight") is True
    assert highlighted[1].get("highlight") is False

def test_optimize_resume_for_job():
    base_resume = {
        "summary": "Developer",
        "skills": ["Python", "Java"],
        "experience": [{"description": "Worked on Python projects."}],
        "education": ["BSc Computer Science"]
    }
    job_desc = "Looking for Python developer."
    optimized = optimize_resume_for_job(base_resume, job_desc)
    assert "python" in optimized["summary"].lower()
    assert optimized["skills"][0].lower() == "python"
    assert optimized["experience"][0].get("highlight") is True
    assert optimized["education"] == base_resume["education"]
