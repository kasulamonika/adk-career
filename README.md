# 🎓 EAMCET Career Agent: Beginner's Guide

Welcome! This project is an AI-powered assistant built with the **Google Agent Development Kit (ADK)**. It helps students find M.Tech colleges in Telangana and generates personalized career roadmaps from graduation to high-paying jobs.

---

## 📂 Project Structure: What's Important?

To run this successfully, you need to know where things live:

*   **`/` (Root Folder)**: This is where you stay most of the time. It contains your environment (`.venv`) and your dependency list (`requirements.txt`).
*   **`eamcet_agent/`**: The "Heart" of the application.
    *   `agent.py`: The main entry point that the ADK looks for.
    *   `.env`: Your secret keys (API Key & DB Password). **Stay here!**
*   **`eamcet_agent/agents/`**: Contains the "specialist" agents (like the Career Coordinator).
*   **`eamcet_agent/tools/`**: The Python functions that talk to the Database and calculate roadmaps.

---

## 🚀 Step-by-Step: How to Run

Follow these steps exactly to get started.

### 1. Open your Terminal in the Root
Make sure your terminal says you are in `/workspaces/adk-career`.

### 2. Create a Virtual Environment (`.venv`)
A virtual environment is like a "sandbox" for this project. It keeps your Python libraries organized.
```bash
python3 -m venv .venv
```

### 3. Activate the Environment
You must "enter" the sandbox before you can use the tools inside it.
```bash
source .venv/bin/activate
```
*(You will see `(.venv)` appear at the start of your command line.)*

### 4. Install the Requirements
Now we install the ADK framework and the Database drivers. **This must happen in the root folder** so that all parts of the project can see them.
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Check your Credentials
The application needs to talk to Google Gemini and the Database. 
*   Check the file `eamcet_agent/.env`.
*   Ensure `GOOGLE_API_KEY` and `DB_PASSWORD` are present.
*   *Note: In this environment, I have already pre-configured these for you.*

### 6. Launch the Application
Run the ADK command from the **Root Folder**. This will scan your project and start the Web UI.
```bash
adk web .
```

---

## 🛠️ How to Use the Agent

Once the command is running:
1.  Click the **"Open in Browser"** popup or go to `http://localhost:8000`.
2.  Type your request in the chat box.

**Try these examples:**
*   *"Which colleges in Hyderabad offer M.Tech in Data Science?"*
*   *"I want to become an AI Engineer. Create a roadmap for me starting from my M.Tech."*

---

## 💡 Important Tips for Beginners

1.  **Where do I install things?** Always run `pip install` from the **Root folder** while your `.venv` is active.
2.  **Where is the ADK?** The ADK is installed inside your `.venv`. You don't need to "install" it into a specific folder; once you activate the environment, the `adk` command is available everywhere.
3.  **Why use the Root?** We run `adk web .` (the dot means "here") from the root so the AI can see the `eamcet_agent` folder and all its tools at once.
4.  **Database Errors?** If you see a database error, run `python3 check_db_schema.py` from the root to test your connection.

---

## ✅ Checklist for Success
- [ ] Terminal is in the Root folder.
- [ ] `.venv` is activated (you see `(.venv)` in the prompt).
- [ ] `pip install -r requirements.txt` finished without errors.
- [ ] `adk web .` is running.
