# EAMCET Agent

Multi-tool ADK agent for searching AICTE-approved M.Tech colleges in Cloud SQL PostgreSQL.

## Overview

This agent provides intelligent search capabilities for M.Tech colleges using Google's ADK framework with Gemini 2.0 Flash. It connects to a Cloud SQL PostgreSQL database and exposes two powerful tools:

- **search_colleges** - Find specific colleges by district
- **count_colleges** - Get statistics on college distribution

## Prerequisites

- Python 3.10+
- Google API Key (from [AI Studio](https://aistudio.google.com/apikey))
- Cloud SQL PostgreSQL credentials (host, database, user, password)

## Setup

### 1. Install Dependencies

```bash
pip install google-adk psycopg2-binary
```

### 2. Configure Environment Variables

Create or update `.env` in the `eamcet_agent/` directory:

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_gemini_api_key_here
DB_PASSWORD=your_cloud_sql_password_here
```

**Security Note:** Never commit `.env` to version control. Use environment variables or secrets management in production.

### 3. Run the Agent

From the parent directory (where `eamcet_agent/` lives):

```bash
adk web .
```

This starts the ADK Web UI at `http://localhost:8000`

## Usage

### Via Web UI

1. Navigate to `http://localhost:8000`
2. Select `eamcet_agent` from the agent list
3. Enter your query in the chat interface

### Example Prompts

- "Find M.Tech colleges in Hyderabad"
- "Show colleges in Warangal"
- "How many AICTE colleges are in Bangalore?"
- "List all colleges available in Telangana"

## Tools

### search_colleges(district: str) → dict

Searches for M.Tech colleges in a specified district.

**Parameters:**
- `district` (str): District name to search for

**Returns:**
```json
{
  "status": "success",
  "data": [
    {
      "NAME": "College Name",
      "ADDRESS": "City, District",
      "COURSE": "M.Tech",
      "INTAKE": 60
    }
  ],
  "count": 1
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Connection error or query failed"
}
```

### count_colleges(district: str) → dict

Counts the number of M.Tech colleges in a specified district.

**Parameters:**
- `district` (str): District name to count

**Returns:**
```json
{
  "status": "success",
  "count": 5
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Connection error or query failed"
}
```

## Architecture

```
┌─────────────────────────┐
│   User Query (adk web)  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Gemini 2.0 Flash LLM   │
│    (Intent Understanding)
└────────────┬────────────┘
             │
        ┌────┴────┐
        │          │
        ▼          ▼
 ┌──────────┐ ┌──────────────┐
 │  search  │ │    count     │
 │ colleges │ │   colleges   │
 └────┬─────┘ └──────┬───────┘
      │              │
      └──────┬───────┘
             ▼
    ┌─────────────────┐
    │  Cloud SQL DB   │
    │  (PostgreSQL)   │
    └─────────────────┘
```

## Database Schema (Expected)

```sql
CREATE TABLE mtech_colleges (
  NAME VARCHAR(255),
  ADDRESS VARCHAR(255),
  DISTRICT VARCHAR(100),
  COURSE VARCHAR(100),
  INTAKE INTEGER
);
```

## Environment Configuration

### Google AI Studio (Free Tier)

Set in `.env`:
```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=AIzaSy...
```

### Vertex AI (Production)

Set in `.env`:
```env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

## Error Handling

The agent gracefully handles:
- Database connection failures
- Invalid district names (returns 0 results)
- SQL syntax errors
- Network timeouts

All errors are returned as structured JSON responses with a `status: "error"` field.

## Development

### Project Structure

```
eamcet_agent/
├── agent.py           # Agent config and database tools
├── __init__.py        # Package initialization
├── .env               # Environment variables (gitignored)
└── README.md          # This file
```

### Adding New Tools

To add a new tool (e.g., `get_college_details`):

1. Define the function in `agent.py`
2. Add it to the `tools=[...]` list in the `root_agent` definition
3. Restart `adk web`

Example:
```python
def get_college_details(college_name: str) -> dict:
    """Get detailed info about a specific college."""
    # Implementation...
    return {"status": "success", "data": {...}}

root_agent = Agent(
    ...
    tools=[search_colleges, count_colleges, get_college_details],
)
```

## Security Best Practices

- ✅ Database password via environment variable (never hardcoded)
- ✅ API key via environment variable
- ✅ `.env` in `.gitignore`
- ✅ Prepared statements (parameterized queries) for SQL injection prevention
- ✅ Error messages don't leak sensitive data

## Troubleshooting

### "adk: command not found"
```bash
pip install google-adk
```

### "ModuleNotFoundError: No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### "Database connection refused"
- Verify Cloud SQL instance IP is correct
- Check database credentials in `.env`
- Confirm network connectivity to Cloud SQL

### Agent not appearing in Web UI
- Ensure you're running from parent directory: `cd .. && adk web .`
- Check both `__init__.py` and `agent.py` exist in `eamcet_agent/`
- Restart the server

## License

Built with Google ADK Python SDK

## Support

For issues with:
- **ADK Framework**: [Google ADK Docs](https://google.github.io/adk-docs/)
- **Gemini API**: [Google AI Studio](https://aistudio.google.com/)
- **Cloud SQL**: [Google Cloud SQL Docs](https://cloud.google.com/sql/docs)
