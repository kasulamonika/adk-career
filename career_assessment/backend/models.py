"""
Pydantic models for the RIASEC Career Assessment API.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    education: Optional[str] = None
    current_role: Optional[str] = None
    skills: Optional[str] = None
    interests: Optional[str] = None
    preferred_region: Optional[str] = None
    learning_speed: Optional[str] = None


class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: str  # A, B, C, or D


class BulkAnswerSubmit(BaseModel):
    answers: List[AnswerSubmit]
