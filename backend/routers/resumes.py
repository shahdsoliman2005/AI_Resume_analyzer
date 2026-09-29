import json
import os
import shutil

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pypdf import PdfReader

import models
import schemas
from database import get_db
from auth_utils import get_current_user
from agents.resume_agent import analyze_resume
from agents.matching_agent import match_resume_to_job

router = APIRouter()

UPLOAD_DIR = "uploads"


def _extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


@router.post("/analyze")
def upload_and_analyze(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
 
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported right now")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file.filename}")
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = _extract_text_from_pdf(path)
    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Couldn't read any text from this file — try a different PDF")

    try:
        analysis = analyze_resume(resume_text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI analysis failed: {str(e)}")

    resume = models.Resume(
        file_path=path,
        extracted_text=resume_text,
        summary=analysis.get("summary", ""),
        skills=json.dumps(analysis.get("technical_skills", []), ensure_ascii=False),
        education=analysis.get("education", ""),
        experience_years=analysis.get("experience_years", 0),
        owner_id=current_user.id,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {"resume_id": resume.id, "analysis": analysis}


@router.get("/", response_model=list[schemas.ResumeOut])
def list_my_resumes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Resume)
        .filter(models.Resume.owner_id == current_user.id)
        .order_by(models.Resume.created_at.desc())
        .all()
    )


@router.get("/{resume_id}/matches", response_model=list[schemas.JobMatchOut])
def get_matches_for_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
   
    resume = (
        db.query(models.Resume)
        .filter(models.Resume.id == resume_id, models.Resume.owner_id == current_user.id)
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    jobs = db.query(models.Job).all()
    results = []
    for job in jobs:
        try:
            match = match_resume_to_job(resume.extracted_text, job.title, job.description)
        except Exception:
            continue

        job_match = models.JobMatch(
            resume_id=resume.id,
            job_id=job.id,
            match_score=match.get("match_score", 0),
            explanation=match.get("explanation", ""),
            missing_skills=json.dumps(match.get("missing_skills", []), ensure_ascii=False),
        )
        db.add(job_match)

        results.append(
            schemas.JobMatchOut(
                job_id=job.id,
                job_title=job.title,
                match_score=match.get("match_score", 0),
                matching_skills=match.get("matching_skills", []),
                missing_skills=match.get("missing_skills", []),
                explanation=match.get("explanation", ""),
            )
        )

    db.commit()
    results.sort(key=lambda r: r.match_score, reverse=True)
    return results
