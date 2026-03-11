"""
FastAPI backend for RIASEC Career Assessment.
Provides REST API endpoints for user management, RIASEC questions,
answer submission, and career roadmap generation.
"""

import hashlib
import os
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .db import (
    init_db,
    get_all_questions,
    get_questions_by_category,
    create_user,
    get_user_by_username,
    get_user_by_id,
    update_user_profile,
    save_answers_bulk,
    get_user_answers,
    calculate_riasec_scores,
    save_assessment_result,
    get_assessment_result,
)
from .models import (
    UserRegister,
    UserLogin,
    UserProfileUpdate,
    BulkAnswerSubmit,
)
from .roadmap import generate_career_roadmap

app = FastAPI(title="RIASEC Career Assessment API", version="1.0.0")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------------
# Startup
# ---------------------
@app.on_event("startup")
def startup():
    init_db()


# ---------------------
# Auth endpoints
# ---------------------
@app.post("/api/register")
def register(user: UserRegister):
    try:
        user_id = create_user(
            user.username, user.email, _hash_password(user.password), user.full_name
        )
        return {"status": "success", "user_id": user_id, "username": user.username}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/login")
def login(user: UserLogin):
    db_user = get_user_by_username(user.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if db_user["password_hash"] != _hash_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {
        "status": "success",
        "user_id": db_user["id"],
        "username": db_user["username"],
        "full_name": db_user["full_name"],
    }


# ---------------------
# Profile endpoints
# ---------------------
@app.get("/api/profile/{user_id}")
def get_profile(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    safe_user = {k: v for k, v in user.items() if k != "password_hash"}
    return {"status": "success", "user": safe_user}


@app.put("/api/profile/{user_id}")
def update_profile(user_id: int, profile: UserProfileUpdate):
    updated = update_user_profile(user_id, **profile.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="User not found or no changes")
    return {"status": "success", "message": "Profile updated"}


# ---------------------
# Questions endpoints
# ---------------------
@app.get("/api/questions")
def list_questions(category: str = None):
    if category:
        questions = get_questions_by_category(category)
    else:
        questions = get_all_questions()
    return {"status": "success", "questions": questions, "count": len(questions)}


# ---------------------
# Answers endpoints
# ---------------------
@app.post("/api/answers/{user_id}")
def submit_answers(user_id: int, payload: BulkAnswerSubmit):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    answers = [a.model_dump() for a in payload.answers]
    save_answers_bulk(user_id, answers)
    return {"status": "success", "message": f"Saved {len(answers)} answers"}


@app.get("/api/answers/{user_id}")
def get_answers(user_id: int):
    answers = get_user_answers(user_id)
    return {"status": "success", "answers": answers, "count": len(answers)}


# ---------------------
# Roadmap endpoint
# ---------------------
@app.get("/api/roadmap/{user_id}")
def get_roadmap(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    answers = get_user_answers(user_id)
    if not answers:
        raise HTTPException(
            status_code=400, detail="No answers found. Please complete the assessment first."
        )

    # Calculate RIASEC scores
    scores = calculate_riasec_scores(user_id)

    # Build user profile for roadmap
    user_profile = {
        "full_name": user.get("full_name"),
        "education": user.get("education"),
        "current_role": user.get("current_role"),
        "skills": user.get("skills", "").split(",") if user.get("skills") else [],
        "interests": user.get("interests", "").split(",") if user.get("interests") else [],
        "learning_speed": user.get("learning_speed", "moderate"),
    }

    # Generate roadmap
    roadmap = generate_career_roadmap(scores, user_profile)

    # Save results
    top_category = roadmap["top_category"]["code"]
    career_rec = ", ".join(roadmap["recommended_careers"][:3])
    save_assessment_result(user_id, scores, top_category, career_rec)

    return {"status": "success", "roadmap": roadmap}


# ---------------------
# Assessment result endpoint
# ---------------------
@app.get("/api/result/{user_id}")
def get_result(user_id: int):
    result = get_assessment_result(user_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No assessment result found. Complete the assessment first.",
        )
    return {"status": "success", "result": result}
