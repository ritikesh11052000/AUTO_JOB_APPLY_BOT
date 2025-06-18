import pytest
from walkin_detection import detect_walkin_in_description, filter_walkin_jobs

def test_detect_walkin_in_description():
    assert detect_walkin_in_description("This is a walk-in interview") == True
    assert detect_walkin_in_description("Immediate joining required") == True
    assert detect_walkin_in_description("On-the-spot hiring") == True
    assert detect_walkin_in_description("Regular job posting") == False
    assert detect_walkin_in_description("") == False

def test_filter_walkin_jobs():
    jobs = [
        {'description': 'This is a walk-in interview for engineers', 'title': 'Engineer'},
        {'description': 'Regular job posting', 'title': 'Manager'},
        {'requirements': 'Immediate joining for sales', 'title': 'Sales Executive'},
        {'description': '', 'title': 'Intern'},
    ]
    filtered = filter_walkin_jobs(jobs)
    assert len(filtered) == 2
    titles = [job['title'] for job in filtered]
    assert 'Engineer' in titles
    assert 'Sales Executive' in titles
    assert 'Manager' not in titles
    assert 'Intern' not in titles
