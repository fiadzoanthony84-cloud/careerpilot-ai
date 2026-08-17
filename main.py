"""
CareerPilot AI — FastAPI bridge (linkedin-clean edition).

Wraps backend/*.py (cv_analyzer, matcher_v3, career_insights,
cover_letter, scam_detector) in the HTTP routes the Streamlit frontend's
api_client.py expects. Uses real LinkedIn job posting data (trimmed to
8,000 postings so it fits GitHub + free-tier hosting).
"""

from __future__ import annotations

import os
import re
import tempfile

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.cv_analyzer import analyze_cv
from backend.matcher_v3 import recommend_jobs
from backend.career_insights import generate_career_insights
from backend.cover_letter import generate_cover_letter
from backend.scam_detector import predict_job

app = FastAPI(title="CareerPilot AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single-user in-memory cache: keeps the last analyzed CV (full analyze_cv()
# output, including raw "text") so /jobs/recommend, /insights, and
# /cover-letter/generate don't need the file re-uploaded each time.
_LAST_CV: dict = {}


def _guess_contact(text: str) -> tuple[str, str]:
    email_match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    phone_match = re.search(r"(\+?\d[\d \-]{7,}\d)", text)
    return (
        email_match.group(0) if email_match else "",
        phone_match.group(0) if phone_match else "",
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/cv/analyze")
async def cv_analyze(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        cv_data = analyze_cv(tmp_path)
    finally:
        os.remove(tmp_path)

    _LAST_CV.clear()
    _LAST_CV.update(cv_data)

    email, phone = _guess_contact(cv_data.get("text", ""))
    education = cv_data.get("education", {})

    # Shape the response to match what the Streamlit frontend expects
    return {
        "name": cv_data.get("name", "Candidate"),
        "email": email,
        "phone": phone,
        "top_qualification": cv_data.get("summary", {}).get("top_qualification", "Not specified"),
        "skills": cv_data.get("skills", []),
        "education": [
            {"degree": q, "institution": "", "year": "", "details": ""}
            for q in education.get("qualifications", [])
        ] or [
            {"degree": inst, "institution": inst, "year": "", "details": ""}
            for inst in education.get("institutions", [])
        ],
        "experience": [
            {"title": e, "company": "", "period": "", "description": ""}
            for e in cv_data.get("experience", [])
        ],
    }


def _clean_salary(value):
    """Cast numpy/NaN salary values to a plain Python float or None."""
    try:
        if value is None:
            return None
        fval = float(value)
        if fval != fval:  # NaN check
            return None
        return fval
    except (TypeError, ValueError):
        return None


@app.post("/api/jobs/recommend")
def jobs_recommend(cv_data: dict = {}):
    if not _LAST_CV:
        return []
    results = recommend_jobs(_LAST_CV, top_n=5)
    output = []
    for i, job in enumerate(results):
        min_sal = _clean_salary(job.get("min_salary"))
        max_sal = _clean_salary(job.get("max_salary"))
        output.append({
            "rank": i + 1,
            "title": str(job["title"]),
            "company": str(job["company"]),
            "location": str(job["location"]),
            "industry": str(job["industry"]),
            "match_score": float(job["score"]),
            "salary": (
                f"{job.get('currency', 'USD')} {min_sal:.0f} - {max_sal:.0f}"
                if min_sal is not None and max_sal is not None
                else "Not specified"
            ),
            "required_skills": [str(s) for s in job.get("skills", [])],
            "missing_skills": [str(s) for s in job.get("missing_skills", [])],
            "description": str(job.get("company_description", "")),
        })
    return output


@app.post("/api/insights")
def insights(cv_data: dict = {}):
    if not _LAST_CV:
        return {"top_industries": [], "missing_skills": [], "salary": {"average": 0, "minimum": 0, "maximum": 0, "distribution": []}}

    data = generate_career_insights(_LAST_CV, top_n=10)

    top_industries = [{"name": name, "count": count, "percentage": 0} for name, count in data["industries"]]
    total = sum(i["count"] for i in top_industries) or 1
    for i in top_industries:
        i["percentage"] = round(i["count"] / total * 100)

    missing_skills = [{"name": name, "demand": count * 10} for name, count in data["missing_skills"]]

    salary = data["salary"]
    return {
        "top_industries": top_industries,
        "missing_skills": missing_skills,
        "salary": {
            "average": salary.get("average") or 0,
            "minimum": salary.get("minimum") or 0,
            "maximum": salary.get("maximum") or 0,
            "distribution": [],
        },
    }


@app.post("/api/cover-letter/generate")
def cover_letter_generate(job: dict, cv: dict):
    if not _LAST_CV:
        return {"letter": "Please analyze a CV first."}
    letter = generate_cover_letter(_LAST_CV, job)
    return {"letter": letter}


@app.post("/api/scam/analyze")
def scam_analyze(payload: dict):
    description = payload.get("description", "")
    prediction, probabilities = predict_job(description)

    legit_pct = round(float(probabilities[0]) * 100, 2)
    fraud_pct = round(float(probabilities[1]) * 100, 2)
    is_scam = prediction == 1

    return {
        "legitimate_pct": legit_pct,
        "fraudulent_pct": fraud_pct,
        "risk_level": "high" if is_scam else ("moderate" if fraud_pct >= 30 else "safe"),
        "risk_label": "HIGH RISK" if is_scam else ("CAUTION" if fraud_pct >= 30 else "SAFE"),
        "risk_icon": "🚨" if is_scam else ("⚠️" if fraud_pct >= 30 else "✅"),
        "details": [f"Model confidence: {fraud_pct}% fraudulent, {legit_pct}% legitimate"],
        "flags": ["Flagged by trained scam-detection model"] if is_scam else [],
    }
