from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class JobRole(str, Enum):
    SOFTWARE_ENGINEER = "Software Engineer"
    AI_ENGINEER = "AI Engineer"
    DATA_ANALYST = "Data Analyst"
    WEB_DEVELOPER = "Web Developer"
    CYBERSECURITY_ANALYST = "Cybersecurity Analyst"


# --- Auth ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- Resume ---
class ResumeOut(BaseModel):
    id: str
    user_id: str
    filename: str
    uploaded_at: datetime
    raw_text_length: int


# --- Analysis ---
class SkillGap(BaseModel):
    skill: str
    importance: str  # "critical" | "important" | "nice-to-have"
    resources: List[str]


class RoadmapPhase(BaseModel):
    phase: int
    title: str
    duration_weeks: int
    goals: List[str]
    skills_to_learn: List[str]
    projects: List[str]
    courses: List[str]


class AnalysisResult(BaseModel):
    resume_id: str
    target_role: str
    ats_score: int = Field(ge=0, le=100)
    strength_score: int = Field(ge=0, le=100)
    match_percentage: int = Field(ge=0, le=100)
    extracted_skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    skill_gaps: List[SkillGap]
    ats_feedback: List[str]
    strengths: List[str]
    weaknesses: List[str]
    roadmap: List[RoadmapPhase]
    interview_questions: List[str]
    summary: str
    created_at: datetime


class AnalysisRequest(BaseModel):
    resume_id: str
    target_role: str  # free text — any job role


# --- Interview ---
class InterviewQuestionRequest(BaseModel):
    resume_id: str
    target_role: str  # free text — any job role
    difficulty: str = "mixed"
