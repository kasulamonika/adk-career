-- RIASEC Career Assessment Database Schema

-- Users table: stores user accounts and profile information
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    age INTEGER,
    education TEXT,
    current_role TEXT,
    skills TEXT,          -- comma-separated skills
    interests TEXT,       -- comma-separated interests
    preferred_region TEXT,
    learning_speed TEXT DEFAULT 'moderate',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RIASEC Questions table: stores MCQ questions categorized by RIASEC type
CREATE TABLE IF NOT EXISTS riasec_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('R','I','A','S','E','C')),
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    -- Each option maps to a score for the RIASEC category
    score_a INTEGER NOT NULL DEFAULT 1,
    score_b INTEGER NOT NULL DEFAULT 2,
    score_c INTEGER NOT NULL DEFAULT 3,
    score_d INTEGER NOT NULL DEFAULT 4,
    difficulty TEXT DEFAULT 'medium' CHECK(difficulty IN ('easy','medium','hard')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Answers table: stores each user's answer per question
CREATE TABLE IF NOT EXISTS user_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    selected_option TEXT NOT NULL CHECK(selected_option IN ('A','B','C','D')),
    score INTEGER NOT NULL,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (question_id) REFERENCES riasec_questions(id),
    UNIQUE(user_id, question_id)
);

-- Assessment Results table: stores computed RIASEC scores per user
CREATE TABLE IF NOT EXISTS assessment_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    realistic_score INTEGER DEFAULT 0,
    investigative_score INTEGER DEFAULT 0,
    artistic_score INTEGER DEFAULT 0,
    social_score INTEGER DEFAULT 0,
    enterprising_score INTEGER DEFAULT 0,
    conventional_score INTEGER DEFAULT 0,
    top_category TEXT,
    career_recommendation TEXT,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
