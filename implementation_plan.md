# Implementation Plan - FastAPI Migration & LangGraph HITL Integration

# Goal Description
Migrate the existing Flask-based AOP Planner application to **FastAPI** to leverage its async capabilities and automatic documentation. unexpected
Integrate **LangGraph** to orchestrate LLM workflows (specifically PRD improvement and RICE analysis).
Implement **Human-in-the-Loop (HITL)** features, allowing users to review and approve AI-generated content before it is finalized.

## User Review Required
> [!IMPORTANT]
> **Architecture Shift**: This is a complete backend migration from Flask to FastAPI. The frontend (Jinja2 templates) can still be served by FastAPI, but API endpoints will change structure slightly.
> **State Management**: LangGraph requires a state store (Checkpointer). We will use an in-memory checkpointer or a simple SQLite based one for this POC to avoid heavy infrastructure dependencies.

## Proposed Changes

### 1. Backend Framework Migration (Flask -> FastAPI)

#### [NEW] [main.py](file:///Users/rasubramani/Documents/My Projects/AOP_branches/AOP-Planner-branch/main.py)
- Re-implement `app.py` functionality using FastAPI.
- Mount static files and templates (using `jinja2`).
- Re-implement Auth endpoints (FastAPI typically uses OAuth2 with JWT, but we can adapt the existing session-based auth or use `authlib` with Starlette/FastAPI session middleware to keep it simple and compatible with existing templates).
- **Strategy**: Keep `flask_login` style session management using `starsessions` or similar to minimize frontend disruption.

#### [NEW] [dependencies.py](file:///Users/rasubramani/Documents/My Projects/AOP_branches/AOP-Planner-branch/dependencies.py)
- Dependency injection for User, Database (JSON helpers), and Settings.

### 2. LangGraph & HITL Integration

#### [NEW] [workflows/prd_agent.py](file:///Users/rasubramani/Documents/My Projects/AOP_branches/AOP-Planner-branch/workflows/prd_agent.py)
- Define a LangGraph `StateGraph`.
- **Nodes**:
    - `analyze_prd`: Analyzes input PRD.
    - `generate_improvement`: Calls LLM to improve PRD.
- **HITL**:
    - Add an `interrupt_before=["commit_improvement"]` or similar breakpoint.
    - The workflow will pause after generation, returning a `thread_id` and the generated content.
    - User (via API) will approve or edit the content.
    - Workflow resumes to save/finalize.

#### [NEW] [routers/workflow.py](file:///Users/rasubramani/Documents/My Projects/AOP_branches/AOP-Planner-branch/routers/workflow.py)
- Endpoints to trigger workflows:
    - `POST /api/workflow/improve-prd`: Starts a graph run. Returns `thread_id` and current state.
    - `GET /api/workflow/{thread_id}/state`: Checks if waiting for input.
    - `POST /api/workflow/{thread_id}/approve`: Sends user approval/edits to resume the graph.

### 3. Dependencies

#### [MODIFY] [requirements.txt](file:///Users/rasubramani/Documents/My Projects/AOP_branches/AOP-Planner-branch/requirements.txt)
- Add: `fastapi`, `uvicorn`, `langgraph`, `langchain-openai`, `python-multipart`, `itsdangerous` (for sessions), `starlette-middleware-sessions` (or equivalent).
- Remove: `flask`, `flask-cors` (replaced by fastapi equivalent).

## Verification Plan

### Automated Tests
- Create a test script `test_workflow.py` to simulate the API flow:
    1. Start workflow -> Expect PAUSED state.
    2. Read state -> Verify generated content exists.
    3. Send generic "approval" -> Verify workflow completes and returns final result.

### Manual Verification
1. **Login**: Verify Google Login works with the new FastAPI backend.
2. **PRD Upload**: Upload a sample PRD via the UI.
3. **Improvement (HITL)**:
    - Click "Improve with AI".
    - **Observe**: The UI should show a "Reviewing..." state or a modal popping up with the AI's proposal (we will need to adjust the frontend JS slightly to handle this 2-step process, or for the POC, we expose the endpoints and verify via Swagger UI).
    - **Action**: Approve the change.
    - **Result**: PRD is updated.
