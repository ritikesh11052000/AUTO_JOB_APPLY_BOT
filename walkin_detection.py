import re
from typing import List, Dict

WALKIN_KEYWORDS = [
    r"walk[- ]in",
    r"immediate joining",
    r"on[- ]the[- ]spot",
]

def detect_walkin_in_description(description: str) -> bool:
    description_lower = description.lower()
    for pattern in WALKIN_KEYWORDS:
        if re.search(pattern, description_lower):
            return True
    return False

def filter_walkin_jobs(jobs: List[Dict]) -> List[Dict]:
    walkin_jobs = []
    for job in jobs:
        description = job.get('description', '') or job.get('requirements', '')
        if description and detect_walkin_in_description(description):
            walkin_jobs.append(job)
    return walkin_jobs
