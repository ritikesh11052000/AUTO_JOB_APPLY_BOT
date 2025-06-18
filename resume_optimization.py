from typing import Dict, List

def extract_job_requirements(job_description: str) -> List[str]:
    # Simple keyword extraction by splitting and filtering common words
    words = job_description.lower().split()
    stopwords = {'and', 'or', 'the', 'a', 'an', 'to', 'for', 'with', 'of', 'in', 'on', 'at', 'by'}
    keywords = [word.strip('.,') for word in words if word not in stopwords and len(word) > 2]
    # Return unique keywords
    return list(set(keywords))

def optimize_summary(base_summary: str, key_requirements: List[str]) -> str:
    # Append key requirements to summary for ATS optimization
    optimized = base_summary
    for req in key_requirements:
        if req not in optimized.lower():
            optimized += f" {req}"
    return optimized.strip()

def prioritize_relevant_skills(base_skills: List[str], key_requirements: List[str]) -> List[str]:
    # Prioritize skills that match key requirements
    prioritized = [skill for skill in base_skills if any(req in skill.lower() for req in key_requirements)]
    # Append other skills
    others = [skill for skill in base_skills if skill not in prioritized]
    return prioritized + others

def highlight_relevant_experience(base_experience: List[Dict], key_requirements: List[str]) -> List[Dict]:
    # Highlight experience entries that mention key requirements
    highlighted = []
    for exp in base_experience:
        description = exp.get('description', '').lower()
        if any(req in description for req in key_requirements):
            exp['highlight'] = True
        else:
            exp['highlight'] = False
        highlighted.append(exp)
    return highlighted

def optimize_resume_for_job(base_resume: Dict, job_description: str) -> Dict:
    key_requirements = extract_job_requirements(job_description)
    optimized_resume = {
        'summary': optimize_summary(base_resume.get('summary', ''), key_requirements),
        'skills': prioritize_relevant_skills(base_resume.get('skills', []), key_requirements),
        'experience': highlight_relevant_experience(base_resume.get('experience', []), key_requirements),
        'education': base_resume.get('education', [])
    }
    return optimized_resume
