"""
Database utilities for the RIASEC Career Assessment system.
Uses SQLite for local storage of users, questions, answers, and results.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "career_assessment.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "schema.sql")
SEED_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "seed_questions.sql")


def get_db():
    """Get a database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize database schema and seed RIASEC questions."""
    conn = get_db()
    cursor = conn.cursor()

    # Create tables
    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())

    # Seed questions if table is empty
    cursor.execute("SELECT COUNT(*) FROM riasec_questions")
    count = cursor.fetchone()[0]
    if count == 0:
        with open(SEED_PATH, "r") as f:
            cursor.executescript(f.read())

    conn.commit()
    conn.close()


def get_all_questions():
    """Fetch all RIASEC questions from the database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, question_text, category, option_a, option_b, option_c, option_d "
        "FROM riasec_questions ORDER BY category, id"
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_questions_by_category(category: str):
    """Fetch questions for a specific RIASEC category."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, question_text, category, option_a, option_b, option_c, option_d "
        "FROM riasec_questions WHERE category = ? ORDER BY id",
        (category.upper(),),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def create_user(username, email, password_hash, full_name):
    """Create a new user account."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, full_name) "
            "VALUES (?, ?, ?, ?)",
            (username, email, password_hash, full_name),
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError as e:
        conn.close()
        raise ValueError(str(e))


def get_user_by_username(username):
    """Find a user by username."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    """Find a user by ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_user_profile(user_id, **kwargs):
    """Update user profile fields."""
    allowed_fields = {
        "full_name", "age", "education", "current_role",
        "skills", "interests", "preferred_region", "learning_speed",
    }
    fields = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}
    if not fields:
        return False

    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [user_id]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE users SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        values,
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def save_answer(user_id, question_id, selected_option):
    """Save or update a user's answer for a question."""
    conn = get_db()
    cursor = conn.cursor()

    # Get the score for the selected option
    score_col = f"score_{selected_option.lower()}"
    cursor.execute(
        f"SELECT {score_col} FROM riasec_questions WHERE id = ?",
        (question_id,),
    )
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise ValueError(f"Question {question_id} not found")

    score = row[0]

    # Upsert answer
    cursor.execute(
        "INSERT INTO user_answers (user_id, question_id, selected_option, score) "
        "VALUES (?, ?, ?, ?) "
        "ON CONFLICT(user_id, question_id) DO UPDATE SET "
        "selected_option = excluded.selected_option, "
        "score = excluded.score, "
        "answered_at = CURRENT_TIMESTAMP",
        (user_id, question_id, selected_option.upper(), score),
    )
    conn.commit()
    conn.close()
    return score


def save_answers_bulk(user_id, answers):
    """Save multiple answers at once. answers is a list of {question_id, selected_option}."""
    conn = get_db()
    cursor = conn.cursor()

    for ans in answers:
        question_id = ans["question_id"]
        selected_option = ans["selected_option"].upper()
        score_col = f"score_{selected_option.lower()}"

        cursor.execute(
            f"SELECT {score_col} FROM riasec_questions WHERE id = ?",
            (question_id,),
        )
        row = cursor.fetchone()
        if not row:
            continue
        score = row[0]

        cursor.execute(
            "INSERT INTO user_answers (user_id, question_id, selected_option, score) "
            "VALUES (?, ?, ?, ?) "
            "ON CONFLICT(user_id, question_id) DO UPDATE SET "
            "selected_option = excluded.selected_option, "
            "score = excluded.score, "
            "answered_at = CURRENT_TIMESTAMP",
            (user_id, question_id, selected_option, score),
        )

    conn.commit()
    conn.close()


def get_user_answers(user_id):
    """Fetch all answers for a user with question details."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT ua.question_id, ua.selected_option, ua.score, "
        "q.question_text, q.category "
        "FROM user_answers ua "
        "JOIN riasec_questions q ON ua.question_id = q.id "
        "WHERE ua.user_id = ? ORDER BY q.category, q.id",
        (user_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def calculate_riasec_scores(user_id):
    """Calculate RIASEC category scores from user's answers."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT q.category, SUM(ua.score) as total_score "
        "FROM user_answers ua "
        "JOIN riasec_questions q ON ua.question_id = q.id "
        "WHERE ua.user_id = ? "
        "GROUP BY q.category",
        (user_id,),
    )
    rows = cursor.fetchall()
    conn.close()

    scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    for row in rows:
        scores[row["category"]] = row["total_score"]

    return scores


def save_assessment_result(user_id, scores, top_category, career_recommendation):
    """Save computed assessment results."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO assessment_results "
        "(user_id, realistic_score, investigative_score, artistic_score, "
        "social_score, enterprising_score, conventional_score, "
        "top_category, career_recommendation) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET "
        "realistic_score = excluded.realistic_score, "
        "investigative_score = excluded.investigative_score, "
        "artistic_score = excluded.artistic_score, "
        "social_score = excluded.social_score, "
        "enterprising_score = excluded.enterprising_score, "
        "conventional_score = excluded.conventional_score, "
        "top_category = excluded.top_category, "
        "career_recommendation = excluded.career_recommendation, "
        "completed_at = CURRENT_TIMESTAMP",
        (
            user_id,
            scores.get("R", 0),
            scores.get("I", 0),
            scores.get("A", 0),
            scores.get("S", 0),
            scores.get("E", 0),
            scores.get("C", 0),
            top_category,
            career_recommendation,
        ),
    )
    conn.commit()
    conn.close()


def get_assessment_result(user_id):
    """Get stored assessment result for a user."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM assessment_results WHERE user_id = ?", (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
