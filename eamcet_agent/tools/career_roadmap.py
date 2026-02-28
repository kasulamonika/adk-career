"""
Career Roadmap Generator with College Data Integration
Generates personalized M.Tech career roadmaps based on user profile and learning speed
"""

from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta


def generate_college_to_career_roadmap(
    user_profile: Dict[str, Any],
    target_specialization: str,
    colleges: List[Dict[str, Any]],
    learning_speed: str = "moderate"
) -> Dict[str, Any]:
    """
    Generate a comprehensive 3-phase roadmap from college selection to career launch.
    
    Args:
        user_profile: Dictionary containing user's background, experience, skills
        target_specialization: Target M.Tech specialization (e.g., "AI/ML", "Data Science")
        colleges: List of college options with details
        learning_speed: "slow", "moderate", or "fast" - affects timeline duration
    
    Returns:
        Dictionary containing:
        - phases: List of 3 phases with detailed breakdown
        - milestones: Key milestones across all phases
        - college_recommendations: Top 3 colleges ranked
        - salary_progression: Salary projection by year
        - success_metrics: Key metrics to track progress
    """
    
    # Timeline multipliers based on learning speed
    speed_multipliers = {
        "slow": 1.3,
        "moderate": 1.0,
        "fast": 0.8
    }
    multiplier = speed_multipliers.get(learning_speed, 1.0)
    
    # Phase 1: Preparation (2-3 months base)
    prep_duration = int(2.5 * multiplier)  # 2-3 months
    phase1_actions = [
        "Research target specialization and career paths",
        "Strengthen foundational concepts (Algorithms, Data Structures, Mathematics)",
        "Prepare for college entrance exams if required",
        "Build portfolio projects in target domain",
        "Network with professionals in specialization",
        "Complete coding challenges and interview prep"
    ]
    
    phase1_deliverables = [
        "Study plan for preparation phase",
        "Portfolio with 2-3 projects",
        "Interview preparation notes",
        "College application completed"
    ]
    
    phase1_success_metrics = [
        "Exam score: 85%+",
        "Portfolio quality: Strong (industry-ready code)",
        "Interview readiness: Moderate to Advanced",
        "College selection: Finalized"
    ]
    
    # Phase 2: M.Tech Studies (24 months with semester breakdown)
    study_duration = int(24 * multiplier)  # 24 months base
    
    semester_breakdown = []
    semester_details = [
        {
            "semester": 1,
            "month_range": "Month 1-4",
            "courses": [
                "Advanced Data Structures",
                "Algorithms & Complexity Analysis",
                "Discrete Mathematics",
                "Specialization Core 1"
            ],
            "projects": ["Data structure implementation", "Algorithm optimization study"],
            "focus": "Foundation building"
        },
        {
            "semester": 2,
            "month_range": "Month 5-8",
            "courses": [
                "Operating Systems",
                "Computer Networks",
                "Specialization Core 2",
                "Elective 1"
            ],
            "projects": ["System design project", "Network protocol implementation"],
            "focus": "Core systems knowledge"
        },
        {
            "semester": 3,
            "month_range": "Month 9-12",
            "courses": [
                "Database Systems",
                "Specialization Advanced 1",
                "Elective 2",
                "Research Methods"
            ],
            "projects": ["Database optimization project", "Research paper review"],
            "focus": "Specialization deepening"
        },
        {
            "semester": 4,
            "month_range": "Month 13-16",
            "courses": [
                "Specialization Advanced 2",
                "Cloud Computing",
                "Elective 3",
                "Industrial Training Prep"
            ],
            "projects": ["Cloud-based application", "Internship preparation"],
            "focus": "Industry alignment"
        },
        {
            "semester": 5,
            "month_range": "Month 17-20",
            "courses": [
                "Advanced Specialization",
                "Capstone Project Part 1",
                "Industry Mentorship",
                "Professional Development"
            ],
            "projects": ["Capstone project initiation", "Industry collaboration"],
            "focus": "Professional growth"
        },
        {
            "semester": 6,
            "month_range": "Month 21-24",
            "courses": [
                "Capstone Project Part 2",
                "Tech Leadership",
                "Final Research",
                "Career Preparation"
            ],
            "projects": ["Capstone completion", "Thesis/Research publication"],
            "focus": "Thesis & career readiness"
        }
    ]
    
    semester_breakdown = semester_details
    
    phase2_actions = [
        "Complete all semester coursework and assignments",
        "Develop industry-relevant projects and portfolio",
        "Participate in internship/industry collaboration",
        "Contribute to research or open-source projects",
        "Build professional network and mentorship connections",
        "Prepare technical and soft skills for placement"
    ]
    
    phase2_deliverables = [
        "6 semester course completions",
        "Capstone project with documentation",
        "Research publication or technical paper",
        "Portfolio with 5+ industry projects",
        "Internship experience report"
    ]
    
    phase2_success_metrics = [
        "GPA: 3.5+/4.0",
        "Project count: 5+ completed",
        "Internship: 1+ (3-6 months)",
        "Publication: 1+ papers/articles",
        "Skills certification: 2+",
        "Interview readiness: Advanced"
    ]
    
    # Phase 3: Career Launch (3-6 months)
    launch_duration = int(4.5 * multiplier)  # 3-6 months
    
    phase3_actions = [
        "Execute targeted job search in specialization",
        "Interview preparation and mock interviews",
        "Negotiate offers and benefits",
        "Plan first-year learning goals",
        "Network with alumni and industry leaders",
        "Start role and establish career trajectory"
    ]
    
    phase3_deliverables = [
        "Job offer from target company",
        "Negotiated compensation package",
        "First-year career plan",
        "Mentor/guide identification",
        "Continuous learning plan"
    ]
    
    phase3_success_metrics = [
        "Job offer obtained: Yes",
        "Salary range achieved: Target met",
        "Company prestige: Top tier preference",
        "Role alignment: 80%+ match",
        "Joining timeline: Within 2 months"
    ]
    
    # Rank colleges based on user profile and specialization
    college_recommendations = rank_colleges(colleges, target_specialization)[:3]
    
    # Generate salary progression
    base_salary = 60  # 60 LPA (Lakhs Per Annum) base
    salary_progression = {
        "M.Tech_start": base_salary,
        "Year_1": base_salary + 5,  # 65 LPA
        "Year_2": base_salary + 12,  # 72 LPA
        "Year_3": base_salary + 20,  # 80 LPA
        "Year_5": base_salary + 35,  # 95 LPA
        "Year_10": base_salary + 60  # 120 LPA
    }
    
    # Construct phases
    phases = [
        {
            "phase": 1,
            "title": "Preparation Phase",
            "duration_months": prep_duration,
            "timeline": f"Month 0-{prep_duration}",
            "monthly_breakdown": [
                {
                    "month": i + 1,
                    "key_activities": phase1_actions[i % len(phase1_actions)],
                    "deliverable": phase1_deliverables[i % len(phase1_deliverables)]
                }
                for i in range(prep_duration)
            ],
            "actions": phase1_actions,
            "deliverables": phase1_deliverables,
            "success_metrics": phase1_success_metrics
        },
        {
            "phase": 2,
            "title": "M.Tech Studies",
            "duration_months": study_duration,
            "timeline": f"Month {prep_duration + 1}-{prep_duration + study_duration}",
            "semester_breakdown": semester_breakdown,
            "monthly_breakdown": [
                {
                    "month": i + 1,
                    "key_activities": phase2_actions[i % len(phase2_actions)],
                    "deliverable": phase2_deliverables[i % len(phase2_deliverables)]
                }
                for i in range(study_duration)
            ],
            "actions": phase2_actions,
            "deliverables": phase2_deliverables,
            "success_metrics": phase2_success_metrics
        },
        {
            "phase": 3,
            "title": "Career Launch",
            "duration_months": launch_duration,
            "timeline": f"Month {prep_duration + study_duration + 1}-{prep_duration + study_duration + launch_duration}",
            "monthly_breakdown": [
                {
                    "month": i + 1,
                    "key_activities": phase3_actions[i % len(phase3_actions)],
                    "deliverable": phase3_deliverables[i % len(phase3_deliverables)]
                }
                for i in range(launch_duration)
            ],
            "actions": phase3_actions,
            "deliverables": phase3_deliverables,
            "success_metrics": phase3_success_metrics
        }
    ]
    
    # Generate milestones
    milestones = [
        {
            "id": "M1",
            "title": "Preparation Phase Complete",
            "month": prep_duration,
            "description": "All foundational preparation completed, college selected"
        },
        {
            "id": "M2",
            "title": "Semester 1 Complete",
            "month": prep_duration + 4,
            "description": "First semester coursework and projects completed"
        },
        {
            "id": "M3",
            "title": "Mid-Degree Review",
            "month": prep_duration + 12,
            "description": "Assessment of progress, GPA check, specialization confirmation"
        },
        {
            "id": "M4",
            "title": "Internship Completion",
            "month": prep_duration + 16,
            "description": "Industry internship or training program completed"
        },
        {
            "id": "M5",
            "title": "Capstone Submission",
            "month": prep_duration + 20,
            "description": "Capstone project completion and documentation"
        },
        {
            "id": "M6",
            "title": "Degree Completion",
            "month": prep_duration + study_duration,
            "description": "M.Tech degree awarded, ready for placement"
        },
        {
            "id": "M7",
            "title": "Job Offer Received",
            "month": prep_duration + study_duration + 2,
            "description": "Job offer from target company in specialization"
        },
        {
            "id": "M8",
            "title": "Career Launch",
            "month": prep_duration + study_duration + launch_duration,
            "description": "New job started, career journey begins"
        }
    ]
    
    # Success metrics summary
    success_metrics = {
        "academic": {
            "target_gpa": "3.5+",
            "completed_courses": 20,
            "projects_completed": 5,
            "publications": "1+"
        },
        "professional": {
            "internships": "1+",
            "industry_certifications": "2+",
            "network_connections": "50+",
            "portfolio_projects": "5+"
        },
        "career": {
            "job_offer": "Guaranteed",
            "salary_target": f"{salary_progression['M.Tech_start']}+ LPA",
            "role_alignment": "80%+",
            "placement_time": "2 months max"
        }
    }
    
    return {
        "phases": phases,
        "milestones": milestones,
        "college_recommendations": college_recommendations,
        "salary_progression": salary_progression,
        "success_metrics": success_metrics,
        "total_duration_months": prep_duration + study_duration + launch_duration,
        "learning_speed_applied": learning_speed,
        "target_specialization": target_specialization
    }


def calculate_career_alignment_score(
    user_profile: Dict[str, Any],
    target_specialization: str
) -> float:
    """
    Calculate career alignment score (0-100) based on user profile and target specialization.
    
    Scoring components:
    - Current role match (20%): How relevant is current role to target specialization
    - Experience level (20%): Years of relevant experience
    - Skills match (30%): Overlap between current and required skills
    - Learning speed (20%): Ability to quickly acquire new skills
    - Interest alignment (10%): Enthusiasm for target specialization
    
    Args:
        user_profile: Dictionary containing user's background, experience, skills, interests
        target_specialization: Target M.Tech specialization
    
    Returns:
        float: Alignment score between 0.0 and 100.0
    """
    
    score = 0.0
    
    # 1. Current Role Match (20%)
    current_role = user_profile.get("current_role", "").lower()
    experience = user_profile.get("experience_years", 0)
    
    role_match_score = 0.0
    role_relevance_map = {
        target_specialization.lower(): 90,
        "software_engineer": 75,
        "data_scientist": 70,
        "ml_engineer": 85,
        "backend_engineer": 65,
        "full_stack_engineer": 60,
        "devops_engineer": 55,
        "student": 50,
        "analyst": 45,
        "manager": 30,
        "sales": 15,
        "finance": 10
    }
    
    for role_key, role_score in role_relevance_map.items():
        if role_key in current_role:
            role_match_score = role_score
            break
    
    if not role_match_score:
        role_match_score = 40  # Default for unmatched roles
    
    score += (role_match_score / 100) * 20
    
    # 2. Experience Level (20%)
    experience_score = min(experience * 10, 100)  # 10 points per year, capped at 100
    score += (experience_score / 100) * 20
    
    # 3. Skills Match (30%)
    user_skills = set([s.lower() for s in user_profile.get("skills", [])])
    specialization_skills = get_specialization_skills(target_specialization)
    
    if user_skills:
        skill_overlap = len(user_skills.intersection(specialization_skills))
        skills_match_percentage = (skill_overlap / len(specialization_skills)) * 100 if specialization_skills else 0
        score += (skills_match_percentage / 100) * 30
    else:
        score += 0  # No skills provided
    
    # 4. Learning Speed (20%)
    learning_speed = user_profile.get("learning_speed", "moderate").lower()
    learning_speed_map = {
        "fast": 90,
        "moderate": 70,
        "slow": 40
    }
    learning_speed_score = learning_speed_map.get(learning_speed, 70)
    score += (learning_speed_score / 100) * 20
    
    # 5. Interest Alignment (10%)
    interests = [i.lower() for i in user_profile.get("interests", [])]
    specialization_keywords = get_specialization_keywords(target_specialization)
    
    interest_match = sum(1 for interest in interests if any(keyword in interest for keyword in specialization_keywords))
    interest_alignment_score = (interest_match / max(len(interests), 1)) * 100 if interests else 50
    score += (min(interest_alignment_score, 100) / 100) * 10
    
    return min(max(score, 0.0), 100.0)


def rank_colleges(
    colleges: List[Dict[str, Any]],
    target_specialization: str
) -> List[Dict[str, Any]]:
    """
    Rank colleges based on their specialization offerings and quality metrics.
    
    Args:
        colleges: List of college dictionaries
        target_specialization: Target specialization to rank by
    
    Returns:
        List of colleges sorted by rank score (descending)
    """
    
    ranked = []
    
    for college in colleges:
        rank_score = 0.0
        
        # Specialization match (40%)
        college_specializations = set([s.lower() for s in college.get("specializations", [])])
        if target_specialization.lower() in college_specializations:
            rank_score += 40
        else:
            rank_score += 15
        
        # NIRF Ranking (30%) - Lower rank number is better
        nirf_rank = college.get("nirf_rank", 999)
        if nirf_rank <= 20:
            rank_score += 30
        elif nirf_rank <= 50:
            rank_score += 25
        elif nirf_rank <= 100:
            rank_score += 20
        else:
            rank_score += 10
        
        # Placement Rate (20%)
        placement_rate = college.get("placement_rate", 70)
        rank_score += (placement_rate / 100) * 20
        
        # Average Salary (10%)
        avg_salary = college.get("average_salary", 60)
        if avg_salary >= 80:
            rank_score += 10
        elif avg_salary >= 60:
            rank_score += 7
        else:
            rank_score += 4
        
        college_copy = college.copy()
        college_copy["rank_score"] = rank_score
        ranked.append(college_copy)
    
    # Sort by rank score descending
    ranked.sort(key=lambda x: x["rank_score"], reverse=True)
    
    return ranked


def get_specialization_skills(specialization: str) -> set:
    """Get required skills for a specialization."""
    
    specialization_skills_map = {
        "ai/ml": {
            "python", "machine learning", "deep learning", "tensorflow", "pytorch",
            "data analysis", "statistics", "nlp", "computer vision", "scikit-learn"
        },
        "data science": {
            "python", "r", "sql", "data analysis", "statistics", "machine learning",
            "data visualization", "pandas", "numpy", "big data", "spark"
        },
        "cloud computing": {
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
            "cloud architecture", "devops", "ci/cd", "microservices"
        },
        "cybersecurity": {
            "network security", "cryptography", "ethical hacking", "penetration testing",
            "security protocols", "firewalls", "intrusion detection", "compliance"
        },
        "blockchain": {
            "solidity", "ethereum", "smart contracts", "distributed systems",
            "cryptography", "consensus algorithms", "web3", "dapps"
        }
    }
    
    spec_lower = specialization.lower()
    for key, skills in specialization_skills_map.items():
        if key in spec_lower:
            return skills
    
    return {"programming", "problem solving", "technical communication"}


def get_specialization_keywords(specialization: str) -> list:
    """Get keywords for a specialization."""
    
    specialization_keywords_map = {
        "ai/ml": ["artificial intelligence", "machine learning", "deep learning", "ai", "ml", "neural"],
        "data science": ["data science", "analytics", "big data", "data engineering", "insights"],
        "cloud computing": ["cloud", "aws", "azure", "gcp", "infrastructure", "devops"],
        "cybersecurity": ["security", "cyber", "hack", "privacy", "protection"],
        "blockchain": ["blockchain", "crypto", "web3", "distributed", "ledger"]
    }
    
    spec_lower = specialization.lower()
    for key, keywords in specialization_keywords_map.items():
        if key in spec_lower:
            return keywords
    
    return ["technology", "engineering", "development"]
