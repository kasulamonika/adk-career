"""
RIASEC Assessment Tools for the ADK Agent.
Reads user data and assessment results from the SQLite database
and provides career recommendations through the agent.
"""

import os
import sys
import sqlite3
from typing import Dict, Any, Optional

DB_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "career_assessment", "db", "career_assessment.db"
)


def _get_db():
    """Connect to the career assessment SQLite database."""
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# RIASEC career mapping used by the agent
RIASEC_CAREER_MAP = {
    "R": {
        "label": "Realistic",
        "careers": [
            "Embedded Systems Engineer", "IoT Developer", "Hardware Engineer",
            "Robotics Engineer", "Network Administrator", "DevOps Engineer",
        ],
        "specializations": [
            "Embedded Systems", "VLSI Design", "Robotics & Automation",
            "Computer Hardware Engineering",
        ],
    },
    "I": {
        "label": "Investigative",
        "careers": [
            "Data Scientist", "ML Engineer", "Research Scientist",
            "AI Engineer", "Cybersecurity Analyst", "Quantitative Analyst",
        ],
        "specializations": [
            "AI & Machine Learning", "Data Science", "Information Security",
            "Computational Mathematics",
        ],
    },
    "A": {
        "label": "Artistic",
        "careers": [
            "UI/UX Designer", "Frontend Developer", "Game Developer",
            "Product Designer", "AR/VR Developer",
        ],
        "specializations": [
            "Human-Computer Interaction", "Computer Graphics",
            "Game Design", "Multimedia Technology",
        ],
    },
    "S": {
        "label": "Social",
        "careers": [
            "Technical Trainer", "Scrum Master", "Community Manager",
            "Technical Writer", "EdTech Product Manager",
        ],
        "specializations": [
            "Educational Technology", "Healthcare Informatics",
            "IT Management", "Communication Systems",
        ],
    },
    "E": {
        "label": "Enterprising",
        "careers": [
            "Product Manager", "Startup Founder", "Business Analyst",
            "IT Consultant", "Program Manager",
        ],
        "specializations": [
            "Technology Management", "Business Analytics",
            "Entrepreneurship", "IT Consulting",
        ],
    },
    "C": {
        "label": "Conventional",
        "careers": [
            "Database Administrator", "QA Engineer", "Systems Analyst",
            "Data Engineer", "Cloud Infrastructure Engineer",
        ],
        "specializations": [
            "Database Management", "Software Quality & Testing",
            "Cloud Computing", "Information Systems",
        ],
    },
}


def get_user_riasec_profile(username: str) -> Dict[str, Any]:
    """
    Retrieve a user's complete RIASEC profile from the assessment database.
    Includes their profile info, assessment scores, and top career category.

    Args:
        username: The username to look up

    Returns:
        dict with user profile, RIASEC scores, top category, and career recommendations
    """
    conn = _get_db()
    if not conn:
        return {"status": "error", "message": "Assessment database not found. Run the assessment first."}

    try:
        cursor = conn.cursor()

        # Get user profile
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_row = cursor.fetchone()
        if not user_row:
            conn.close()
            return {"status": "error", "message": f"User '{username}' not found"}

        user = dict(user_row)
        user_id = user["id"]

        # Get assessment result
        cursor.execute("SELECT * FROM assessment_results WHERE user_id = ?", (user_id,))
        result_row = cursor.fetchone()

        if not result_row:
            # Calculate from answers
            cursor.execute(
                "SELECT q.category, SUM(ua.score) as total_score "
                "FROM user_answers ua "
                "JOIN riasec_questions q ON ua.question_id = q.id "
                "WHERE ua.user_id = ? GROUP BY q.category",
                (user_id,),
            )
            score_rows = cursor.fetchall()
            if not score_rows:
                conn.close()
                return {"status": "error", "message": "No assessment answers found for this user"}

            scores = {r["category"]: r["total_score"] for r in score_rows}
        else:
            result = dict(result_row)
            scores = {
                "R": result["realistic_score"],
                "I": result["investigative_score"],
                "A": result["artistic_score"],
                "S": result["social_score"],
                "E": result["enterprising_score"],
                "C": result["conventional_score"],
            }

        conn.close()

        # Determine top category
        top_cat = max(scores, key=scores.get)
        sorted_cats = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        total = sum(scores.values()) or 1

        career_info = RIASEC_CAREER_MAP.get(top_cat, {})

        return {
            "status": "success",
            "user": {
                "username": user["username"],
                "full_name": user["full_name"],
                "education": user.get("education"),
                "current_role": user.get("current_role"),
                "skills": user.get("skills"),
                "interests": user.get("interests"),
                "learning_speed": user.get("learning_speed"),
            },
            "riasec_scores": scores,
            "score_percentages": {
                RIASEC_CAREER_MAP[k]["label"]: round((v / total) * 100, 1)
                for k, v in scores.items()
            },
            "top_category": {
                "code": top_cat,
                "label": career_info.get("label", "Unknown"),
            },
            "top_3_categories": [
                {"code": cat, "label": RIASEC_CAREER_MAP[cat]["label"], "score": sc}
                for cat, sc in sorted_cats[:3]
            ],
            "recommended_careers": career_info.get("careers", []),
            "recommended_specializations": career_info.get("specializations", []),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if conn:
            conn.close()


def get_riasec_career_recommendation(category: str) -> Dict[str, Any]:
    """
    Get detailed career recommendations for a specific RIASEC category.

    Args:
        category: One of R, I, A, S, E, C

    Returns:
        dict with career paths, specializations, and development advice for that category
    """
    cat = category.upper()
    if cat not in RIASEC_CAREER_MAP:
        return {"status": "error", "message": f"Invalid category '{category}'. Use R, I, A, S, E, or C."}

    info = RIASEC_CAREER_MAP[cat]
    return {
        "status": "success",
        "category": cat,
        "label": info["label"],
        "recommended_careers": info["careers"],
        "recommended_specializations": info["specializations"],
    }


def list_assessment_users() -> Dict[str, Any]:
    """
    List all users who have completed the RIASEC assessment.

    Returns:
        dict with list of users and their top RIASEC category
    """
    conn = _get_db()
    if not conn:
        return {"status": "error", "message": "Assessment database not found"}

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT u.username, u.full_name, ar.top_category, ar.career_recommendation "
            "FROM assessment_results ar "
            "JOIN users u ON ar.user_id = u.id "
            "ORDER BY ar.completed_at DESC"
        )
        rows = cursor.fetchall()
        conn.close()

        users = []
        for row in rows:
            r = dict(row)
            cat = r.get("top_category", "")
            label = RIASEC_CAREER_MAP.get(cat, {}).get("label", "Unknown")
            users.append({
                "username": r["username"],
                "full_name": r["full_name"],
                "top_category": f"{cat} ({label})",
                "career_recommendation": r["career_recommendation"],
            })

        return {"status": "success", "users": users, "count": len(users)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if conn:
            conn.close()
