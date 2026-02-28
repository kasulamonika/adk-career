import psycopg2
from psycopg2.extras import RealDictCursor
import os
from typing import Dict, List, Any

def get_db_connection():
    return psycopg2.connect(
        host="34.27.117.60",
        database="eamcet_db",
        user="postgres",
        password=os.getenv("DB_PASSWORD"),
        port=5432
    )

# ========================
# CAREER DISCOVERY TOOLS
# ========================

def search_career_specializations(interest: str) -> Dict[str, Any]:
    """
    Search for available M.Tech specializations matching user interest.
    
    Args:
        interest: User's career interest (e.g., 'AI', 'Data Science', 'Cloud')
        
    Returns:
        dict with matching specializations and college count per specialization
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT DISTINCT "COURSE", COUNT(*) as colleges_offering, 
                   SUM(CAST("INTAKE" as INTEGER)) as total_intake
            FROM mtech_colleges
            WHERE "COURSE" IS NOT NULL 
              AND "COURSE" != 'COURSE'
              AND LOWER("COURSE") LIKE %s
            GROUP BY "COURSE"
            ORDER BY colleges_offering DESC
            LIMIT 5
        """
        
        cursor.execute(query, (f"%{interest.lower()}%",))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {
            "status": "success",
            "specializations": [dict(row) for row in results],
            "count": len(results)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_colleges_for_specialization(specialization: str, district: str = None) -> Dict[str, Any]:
    """
    Get colleges offering a specific specialization.
    
    Args:
        specialization: Course name (e.g., 'Artificial Intelligence')
        district: Optional filter by district
        
    Returns:
        dict with colleges, intake, and location details
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        if district:
            query = """
                SELECT "NAME", "DISTRICT", "COURSE", "INTAKE", "ENROLLMENT",
                       "INSTITUTION TYPE", "UNIVERSITY"
                FROM mtech_colleges
                WHERE LOWER("COURSE") LIKE %s 
                  AND LOWER("DISTRICT") LIKE %s
                  AND "COURSE" != 'COURSE'
                ORDER BY "INTAKE" DESC
                LIMIT 10
            """
            cursor.execute(query, (f"%{specialization.lower()}%", f"%{district.lower()}%"))
        else:
            query = """
                SELECT "NAME", "DISTRICT", "COURSE", "INTAKE", "ENROLLMENT",
                       "INSTITUTION TYPE", "UNIVERSITY"
                FROM mtech_colleges
                WHERE LOWER("COURSE") LIKE %s 
                  AND "COURSE" != 'COURSE'
                ORDER BY "DISTRICT", "INTAKE" DESC
                LIMIT 15
            """
            cursor.execute(query, (f"%{specialization.lower()}%",))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {
            "status": "success",
            "colleges": [dict(row) for row in results],
            "count": len(results)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def analyze_career_popularity(interest_area: str = None) -> Dict[str, Any]:
    """
    Analyze which specializations are most popular (more colleges, more intake).
    
    Args:
        interest_area: Optional filter (e.g., 'AI', 'Data', 'Cloud')
        
    Returns:
        dict with most popular specializations ranked by demand
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        if interest_area:
            query = """
                SELECT "COURSE", COUNT(*) as colleges, 
                       SUM(CAST("INTAKE" as INTEGER)) as total_seats,
                       COUNT(DISTINCT "DISTRICT") as regions
                FROM mtech_colleges
                WHERE "COURSE" IS NOT NULL 
                  AND "COURSE" != 'COURSE'
                  AND LOWER("COURSE") LIKE %s
                GROUP BY "COURSE"
                ORDER BY colleges DESC, total_seats DESC
                LIMIT 10
            """
            cursor.execute(query, (f"%{interest_area.lower()}%",))
        else:
            query = """
                SELECT "COURSE", COUNT(*) as colleges, 
                       SUM(CAST("INTAKE" as INTEGER)) as total_seats,
                       COUNT(DISTINCT "DISTRICT") as regions
                FROM mtech_colleges
                WHERE "COURSE" IS NOT NULL AND "COURSE" != 'COURSE'
                GROUP BY "COURSE"
                ORDER BY colleges DESC, total_seats DESC
                LIMIT 20
            """
            cursor.execute(query)
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Rank by demand
        for idx, row in enumerate(results, 1):
            row['demand_rank'] = idx
        
        return {
            "status": "success",
            "popular_specializations": [dict(row) for row in results],
            "count": len(results)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_regional_opportunities(user_district: str) -> Dict[str, Any]:
    """
    Get available opportunities in user's preferred region.
    
    Args:
        user_district: User's district preference
        
    Returns:
        dict with colleges and specializations available in region
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get colleges by district
        query = """
            SELECT "DISTRICT", COUNT(*) as total_colleges,
                   COUNT(DISTINCT "COURSE") as unique_courses,
                   SUM(CAST("INTAKE" as INTEGER)) as total_seats
            FROM mtech_colleges
            WHERE LOWER("DISTRICT") LIKE %s
              AND "COURSE" != 'COURSE'
            GROUP BY "DISTRICT"
        """
        
        cursor.execute(query, (f"%{user_district.lower()}%",))
        district_stats = cursor.fetchone()
        
        # Get top specializations in this region
        query2 = """
            SELECT "COURSE", COUNT(*) as colleges,
                   SUM(CAST("INTAKE" as INTEGER)) as seats
            FROM mtech_colleges
            WHERE LOWER("DISTRICT") LIKE %s
              AND "COURSE" != 'COURSE'
            GROUP BY "COURSE"
            ORDER BY colleges DESC
            LIMIT 10
        """
        
        cursor.execute(query2, (f"%{user_district.lower()}%",))
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {
            "status": "success",
            "district": dict(district_stats) if district_stats else None,
            "top_courses": [dict(row) for row in courses],
            "total_courses": len(courses)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def match_skills_to_specializations(user_skills: List[str]) -> Dict[str, Any]:
    """
    Match user's current skills to relevant specializations.
    
    Args:
        user_skills: List of user's skills (e.g., ['Python', 'AI', 'Statistics'])
        
    Returns:
        dict with recommended specializations ranked by relevance
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get all specializations
        query = """
            SELECT DISTINCT "COURSE", COUNT(*) as colleges
            FROM mtech_colleges
            WHERE "COURSE" IS NOT NULL AND "COURSE" != 'COURSE'
            GROUP BY "COURSE"
            ORDER BY colleges DESC
        """
        
        cursor.execute(query)
        all_courses = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Rank specializations by relevance to user skills
        recommendations = []
        for course in all_courses:
            course_name = course['COURSE'].lower()
            relevance_score = 0
            matched_skills = []
            
            for skill in user_skills:
                if skill.lower() in course_name:
                    relevance_score += 2
                    matched_skills.append(skill)
            
            if relevance_score > 0:
                course_dict = dict(course)
                course_dict['relevance_score'] = relevance_score
                course_dict['matched_skills'] = matched_skills
                recommendations.append(course_dict)
        
        # Sort by relevance
        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return {
            "status": "success",
            "recommended_specializations": recommendations[:10],
            "match_count": len(recommendations)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_growth_specializations() -> Dict[str, Any]:
    """
    Identify high-growth specializations based on college offering counts.
    High availability = high demand = good career prospects.
    
    Returns:
        dict with growth potential specializations
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT "COURSE", COUNT(*) as colleges_offering,
                   COUNT(DISTINCT "DISTRICT") as regions,
                   SUM(CAST("INTAKE" as INTEGER)) as total_intake
            FROM mtech_colleges
            WHERE "COURSE" IS NOT NULL AND "COURSE" != 'COURSE'
            GROUP BY "COURSE"
            HAVING COUNT(*) >= 3
            ORDER BY colleges_offering DESC, total_intake DESC
            LIMIT 15
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Mark growth specializations
        growth_sectors = []
        for row in results:
            course_dict = dict(row)
            # Calculate growth score (more colleges + more regions = high growth)
            growth_score = (course_dict['colleges_offering'] * 10 + 
                           course_dict['regions'] * 5)
            course_dict['growth_score'] = growth_score
            growth_sectors.append(course_dict)
        
        return {
            "status": "success",
            "high_growth_sectors": growth_sectors,
            "count": len(growth_sectors)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
