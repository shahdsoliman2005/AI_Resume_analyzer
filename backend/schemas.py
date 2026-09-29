from pydantic import BaseModel
from typing import Optional


# ---------- Auth ----------
class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# ---------- Resumes ----------
class ResumeAnalysis(BaseModel):
    summary: str
    technical_skills: list[str]
    soft_skills: list[str]
    education: str
    experience_years: int


class ResumeOut(BaseModel):
    id: int
    summary: Optional[str] = None
    education: Optional[str] = None
    experience_years: Optional[int] = None
    created_at: object

    class Config:
        from_attributes = True


# ---------- Jobs ----------
class JobCreate(BaseModel):
    title: str
    company: str
    description: str
    required_skills: list[str]
    location: Optional[str] = None


class JobOut(BaseModel):
    id: int
    title: str
    company: Optional[str]
    description: str
    required_skills: Optional[str]
    location: Optional[str]

    class Config:
        from_attributes = True


class JobMatchOut(BaseModel):
    job_id: int
    job_title: str
    match_score: float
    matching_skills: list[str]
    missing_skills: list[str]
    explanation: str


# ---------- Career Advisor ----------
class AdviceRequest(BaseModel):
    question: str


class AdviceResponse(BaseModel):
    answer: str
