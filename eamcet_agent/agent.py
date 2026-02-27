import os
import psycopg2
from psycopg2.extras import RealDictCursor
from google.adk.agents.llm_agent import Agent

# ========================
# DATABASE CONFIGURATION
# ========================
DB_CONFIG = {
    "host": "34.27.117.60",
    "database": "eamcet_db",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "port": 5432
}

# ========================
# DATABASE TOOLS
# ========================

def search_colleges(district: str) -> dict:
    """
    Searches M.Tech colleges in a given district.
    
    Args:
        district: District name to search for
        
    Returns:
        dict with status and college data or error message
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT "NAME", "ADDRESS", "COURSE", "INTAKE" 
            FROM mtech_colleges 
            WHERE "DISTRICT" ILIKE %s 
            LIMIT 5;
        """
        
        cursor.execute(query, (f"%{district}%",))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            "status": "success",
            "data": results,
            "count": len(results)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def count_colleges(district: str) -> dict:
    """
    Counts M.Tech colleges in a given district.
    
    Args:
        district: District name to count
        
    Returns:
        dict with status and college count or error message
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = """
            SELECT COUNT(*) 
            FROM mtech_colleges 
            WHERE "DISTRICT" ILIKE %s;
        """
        
        cursor.execute(query, (f"%{district}%",))
        count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return {
            "status": "success",
            "count": count
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ========================
# AGENT CONFIGURATION
# ========================

root_agent = Agent(
    model="gemini-2.0-flash",
    name="eamcet_agent",
    description="Agent that searches AICTE approved M.Tech colleges in Cloud SQL.",
    instruction=(
        "You are an assistant that helps users find AICTE approved M.Tech colleges. "
        "When users ask about colleges in a specific district, use the search_colleges tool to fetch data. "
        "If they ask for counts or statistics, use the count_colleges tool. "
        "Always provide clear information about college name, address, course, and intake capacity."
    ),
    tools=[search_colleges, count_colleges],
)
