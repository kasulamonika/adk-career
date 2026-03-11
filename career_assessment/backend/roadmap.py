"""
RIASEC Career Roadmap Generator.
Maps RIASEC scores to career paths and generates personalized roadmaps.
"""

# RIASEC category full names
RIASEC_LABELS = {
    "R": "Realistic",
    "I": "Investigative",
    "A": "Artistic",
    "S": "Social",
    "E": "Enterprising",
    "C": "Conventional",
}

# Career paths mapped to RIASEC categories
CAREER_MAP = {
    "R": {
        "title": "Realistic — The Builder",
        "description": (
            "You prefer practical, hands-on work and enjoy building, repairing, "
            "or working with tools, machines, and physical systems."
        ),
        "careers": [
            "Embedded Systems Engineer",
            "IoT Developer",
            "Hardware Engineer",
            "Robotics Engineer",
            "Network Administrator",
            "DevOps / Infrastructure Engineer",
            "Civil / Mechanical Engineer",
        ],
        "specializations": [
            "Embedded Systems",
            "VLSI Design",
            "Robotics & Automation",
            "Computer Hardware Engineering",
            "Structural Engineering",
        ],
        "skills_to_develop": [
            "C/C++ Programming",
            "Microcontroller Programming",
            "CAD Tools",
            "Linux Systems Administration",
            "Networking Protocols",
        ],
    },
    "I": {
        "title": "Investigative — The Thinker",
        "description": (
            "You are analytical, curious, and enjoy solving complex problems "
            "through research, data analysis, and scientific inquiry."
        ),
        "careers": [
            "Data Scientist",
            "Machine Learning Engineer",
            "Research Scientist",
            "AI Engineer",
            "Bioinformatics Specialist",
            "Quantitative Analyst",
            "Cybersecurity Analyst",
        ],
        "specializations": [
            "Artificial Intelligence & Machine Learning",
            "Data Science & Analytics",
            "Computational Mathematics",
            "Information Security",
            "Bioinformatics",
        ],
        "skills_to_develop": [
            "Python & R Programming",
            "Statistics & Probability",
            "Machine Learning Frameworks",
            "Research Methodology",
            "Critical Thinking",
        ],
    },
    "A": {
        "title": "Artistic — The Creator",
        "description": (
            "You are creative, expressive, and enjoy designing, visualizing, "
            "and bringing innovative ideas to life."
        ),
        "careers": [
            "UI/UX Designer",
            "Frontend Developer",
            "Game Developer",
            "Product Designer",
            "Creative Technologist",
            "Motion Graphics Designer",
            "AR/VR Developer",
        ],
        "specializations": [
            "Human-Computer Interaction",
            "Computer Graphics & Visualization",
            "Game Design & Development",
            "Multimedia Technology",
            "AR/VR Technology",
        ],
        "skills_to_develop": [
            "Design Thinking",
            "Figma / Adobe Creative Suite",
            "JavaScript & React",
            "3D Modeling & Animation",
            "User Research",
        ],
    },
    "S": {
        "title": "Social — The Helper",
        "description": (
            "You are empathetic, communicative, and enjoy working with people — "
            "teaching, mentoring, counseling, or collaborating in teams."
        ),
        "careers": [
            "Technical Trainer / Educator",
            "Scrum Master / Agile Coach",
            "Community Manager",
            "Technical Writer",
            "HR Tech Specialist",
            "Healthcare IT Specialist",
            "EdTech Product Manager",
        ],
        "specializations": [
            "Educational Technology",
            "Healthcare Informatics",
            "IT Management",
            "Software Project Management",
            "Communication Systems",
        ],
        "skills_to_develop": [
            "Communication & Presentation",
            "Team Leadership",
            "Instructional Design",
            "Empathy & Active Listening",
            "Conflict Resolution",
        ],
    },
    "E": {
        "title": "Enterprising — The Leader",
        "description": (
            "You are ambitious, persuasive, and enjoy leading teams, making "
            "business decisions, and driving growth."
        ),
        "careers": [
            "Product Manager",
            "Startup Founder / Entrepreneur",
            "Technical Sales Engineer",
            "Business Analyst",
            "IT Consultant",
            "Venture Capital Analyst",
            "Program Manager",
        ],
        "specializations": [
            "Technology Management",
            "Business Analytics",
            "Entrepreneurship & Innovation",
            "IT Strategy & Consulting",
            "Digital Marketing Technology",
        ],
        "skills_to_develop": [
            "Strategic Thinking",
            "Negotiation & Persuasion",
            "Financial Modeling",
            "Product Roadmap Planning",
            "Market Analysis",
        ],
    },
    "C": {
        "title": "Conventional — The Organizer",
        "description": (
            "You are detail-oriented, methodical, and enjoy working with data, "
            "processes, and structured systems."
        ),
        "careers": [
            "Database Administrator",
            "Quality Assurance Engineer",
            "Systems Analyst",
            "ERP Consultant",
            "Compliance / Audit Analyst",
            "Cloud Infrastructure Engineer",
            "Data Engineer",
        ],
        "specializations": [
            "Database Management Systems",
            "Software Quality & Testing",
            "Enterprise Systems",
            "Cloud Computing & DevOps",
            "Information Systems Management",
        ],
        "skills_to_develop": [
            "SQL & Database Design",
            "Process Optimization",
            "Quality Assurance Frameworks",
            "Cloud Platforms (AWS/Azure/GCP)",
            "Documentation & Standards",
        ],
    },
}


def generate_career_roadmap(scores, user_profile=None):
    """
    Generate a personalized career roadmap based on RIASEC scores.

    Args:
        scores: dict with keys R, I, A, S, E, C and integer score values
        user_profile: optional dict with user's profile information

    Returns:
        dict with complete roadmap including career paths, phases, and recommendations
    """
    # Determine top categories
    sorted_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_category = sorted_categories[0][0]
    secondary_category = sorted_categories[1][0] if len(sorted_categories) > 1 else None

    top_info = CAREER_MAP[top_category]
    secondary_info = CAREER_MAP.get(secondary_category, {})

    # Calculate percentages
    total = sum(scores.values()) or 1
    score_percentages = {
        RIASEC_LABELS[k]: round((v / total) * 100, 1) for k, v in scores.items()
    }

    # Build roadmap phases
    learning_speed = "moderate"
    if user_profile:
        learning_speed = user_profile.get("learning_speed", "moderate") or "moderate"

    speed_multipliers = {"slow": 1.3, "moderate": 1.0, "fast": 0.8}
    multiplier = speed_multipliers.get(learning_speed, 1.0)

    phases = [
        {
            "phase": 1,
            "title": "Self-Assessment & Skill Gap Analysis",
            "duration_months": max(1, int(2 * multiplier)),
            "actions": [
                "Review your RIASEC results and identify your strengths",
                f"Research careers in the {top_info['title']} domain",
                "Identify skill gaps compared to target careers",
                "Set up a learning plan with clear milestones",
                "Join online communities in your target field",
            ],
        },
        {
            "phase": 2,
            "title": "Foundation & Skill Building",
            "duration_months": max(3, int(6 * multiplier)),
            "actions": [
                f"Start learning: {', '.join(top_info['skills_to_develop'][:3])}",
                "Complete 2-3 online courses or certifications",
                "Build 2 portfolio projects in your target domain",
                "Participate in hackathons or coding challenges",
                "Connect with mentors in your target career path",
            ],
        },
        {
            "phase": 3,
            "title": "Specialization & Advanced Learning",
            "duration_months": max(3, int(6 * multiplier)),
            "actions": [
                f"Deep-dive into specialization: {top_info['specializations'][0]}",
                "Complete an advanced course or M.Tech preparation",
                "Contribute to open-source or research projects",
                "Build an industry-relevant capstone project",
                "Start applying for internships or entry-level roles",
            ],
        },
        {
            "phase": 4,
            "title": "Career Launch & Growth",
            "duration_months": max(2, int(4 * multiplier)),
            "actions": [
                "Apply for target roles and prepare for interviews",
                "Build your professional network on LinkedIn",
                "Negotiate offers and choose the best fit",
                "Plan your first-year growth objectives",
                "Set up a continuous learning routine",
            ],
        },
    ]

    total_duration = sum(p["duration_months"] for p in phases)

    # Build salary progression estimate
    salary_progression = {
        "Entry Level": "4-8 LPA",
        "Year 2": "8-15 LPA",
        "Year 5": "15-30 LPA",
        "Year 10": "30-60+ LPA",
    }

    roadmap = {
        "riasec_scores": scores,
        "score_percentages": score_percentages,
        "top_category": {
            "code": top_category,
            "label": RIASEC_LABELS[top_category],
            "info": top_info,
        },
        "secondary_category": {
            "code": secondary_category,
            "label": RIASEC_LABELS.get(secondary_category, ""),
            "info": secondary_info,
        }
        if secondary_category
        else None,
        "recommended_careers": top_info["careers"],
        "recommended_specializations": top_info["specializations"],
        "skills_to_develop": top_info["skills_to_develop"],
        "roadmap_phases": phases,
        "total_duration_months": total_duration,
        "learning_speed": learning_speed,
        "salary_progression": salary_progression,
    }

    return roadmap
