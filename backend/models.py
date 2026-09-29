from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("Resume", back_populates="owner", cascade="all, delete-orphan")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    extracted_text = Column(Text)
    summary = Column(Text)
    skills = Column(Text)          # JSON string holding the list of skills
    education = Column(Text)
    experience_years = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="resumes")
    matches = relationship("JobMatch", back_populates="resume", cascade="all, delete-orphan")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String)
    description = Column(Text, nullable=False)
    required_skills = Column(Text)   # JSON string
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    matches = relationship("JobMatch", back_populates="job", cascade="all, delete-orphan")


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    match_score = Column(Float)
    explanation = Column(Text)
    missing_skills = Column(Text)   # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    resume = relationship("Resume", back_populates="matches")
    job = relationship("Job", back_populates="matches")
