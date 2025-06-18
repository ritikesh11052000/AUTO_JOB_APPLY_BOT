import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

PDF_STORAGE_DIR = "resumes"

def generate_pdf_resume(resume_data: dict, company_name: str, job_title: str) -> str:
    if not os.path.exists(PDF_STORAGE_DIR):
        os.makedirs(PDF_STORAGE_DIR)

    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"Resume_{company_name}_{job_title}_{date_str}.pdf"
    filepath = os.path.join(PDF_STORAGE_DIR, filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"Resume for {job_title} at {company_name}")
    y -= 30

    c.setFont("Helvetica", 12)
    # Summary
    summary = resume_data.get("summary", "")
    c.drawString(50, y, "Summary:")
    y -= 20
    for line in summary.split('\n'):
        c.drawString(60, y, line)
        y -= 15

    y -= 10
    # Skills
    skills = resume_data.get("skills", [])
    c.drawString(50, y, "Skills:")
    y -= 20
    c.drawString(60, y, ", ".join(skills))
    y -= 30

    # Experience
    experience = resume_data.get("experience", [])
    c.drawString(50, y, "Experience:")
    y -= 20
    for exp in experience:
        title = exp.get("title", "N/A")
        desc = exp.get("description", "")
        c.drawString(60, y, f"- {title}")
        y -= 15
        for line in desc.split('\n'):
            c.drawString(70, y, line)
            y -= 15
        y -= 10
        if y < 100:
            c.showPage()
            y = height - 50

    # Education
    education = resume_data.get("education", [])
    c.drawString(50, y, "Education:")
    y -= 20
    for edu in education:
        c.drawString(60, y, f"- {edu}")
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
    return filepath
