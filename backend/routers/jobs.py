import json
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from auth_utils import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.JobOut)
def add_job(
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    new_job = models.Job(
        title=job.title,
        company=job.company,
        description=job.description,
        required_skills=json.dumps(job.required_skills, ensure_ascii=False),
        location=job.location,
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


@router.get("/", response_model=list[schemas.JobOut])
def list_jobs(
    q: Optional[str] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db),
):
   
    query = db.query(models.Job)
    if q:
        query = query.filter(models.Job.title.ilike(f"%{q}%"))
    if location:
        query = query.filter(models.Job.location.ilike(f"%{location}%"))
    return query.order_by(models.Job.created_at.desc()).all()


@router.get("/{job_id}", response_model=schemas.JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=schemas.JobOut)
def update_job(
    job_id: int,
    job_update: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.title = job_update.title
    job.company = job_update.company
    job.description = job_update.description
    job.required_skills = json.dumps(job_update.required_skills, ensure_ascii=False)
    job.location = job_update.location

    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
  
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}
