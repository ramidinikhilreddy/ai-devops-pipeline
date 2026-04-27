from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AI DevOps Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NOW = datetime.now(timezone.utc)

JIRA_TICKETS: List[Dict[str, Any]] = [
    {
        "key": "KAN-3",
        "title": "Dashboard Charts",
        "summary": "Build Jira and pipeline KPI cards with charts.",
        "status": "To Do",
        "priority": "Medium",
        "assignee": "Mahdi",
        "type": "Story",
        "labels": ["frontend", "dashboard"],
        "created": (NOW - timedelta(days=8)).isoformat(),
        "updated": (NOW - timedelta(hours=6)).isoformat(),
        "description": "Create total ticket, active runs, failed tests, open PR, and agent activity widgets.",
    },
    {
        "key": "KAN-6",
        "title": "Email Notifications",
        "summary": "Add pipeline result notifications.",
        "status": "To Do",
        "priority": "Low",
        "assignee": "Amina",
        "type": "Task",
        "labels": ["backend", "notifications"],
        "created": (NOW - timedelta(days=4)).isoformat(),
        "updated": (NOW - timedelta(hours=4)).isoformat(),
        "description": "Send summaries for failed runs, PR approvals, and AI actions.",
    },
    {
        "key": "KAN-9",
        "title": "Admin Panel",
        "summary": "Secure settings and provider controls.",
        "status": "To Do",
        "priority": "High",
        "assignee": "Sara",
        "type": "Epic",
        "labels": ["security", "settings"],
        "created": (NOW - timedelta(days=6)).isoformat(),
        "updated": (NOW - timedelta(hours=8)).isoformat(),
        "description": "Manage Jira, GitHub, LLM, and vector DB integrations from a single page.",
    },
    {
        "key": "KAN-2",
        "title": "User Registration API",
        "summary": "Ship FastAPI auth registration flow.",
        "status": "In Progress",
        "priority": "High",
        "assignee": "Mahdi",
        "type": "Story",
        "labels": ["auth", "backend"],
        "created": (NOW - timedelta(days=7)).isoformat(),
        "updated": (NOW - timedelta(hours=1)).isoformat(),
        "description": "Implement validation, hashing, and success/error responses.",
    },
    {
        "key": "KAN-7",
        "title": "Profile Settings",
        "summary": "Allow user profile updates from settings page.",
        "status": "In Progress",
        "priority": "Medium",
        "assignee": "Lina",
        "type": "Task",
        "labels": ["frontend", "settings"],
        "created": (NOW - timedelta(days=5)).isoformat(),
        "updated": (NOW - timedelta(hours=2)).isoformat(),
        "description": "Support profile metadata and integration preferences.",
    },
    {
        "key": "KAN-5",
        "title": "Payment Integration",
        "summary": "Complete gateway integration and tests.",
        "status": "In Review",
        "priority": "Highest",
        "assignee": "Omar",
        "type": "Bug",
        "labels": ["payments", "api"],
        "created": (NOW - timedelta(days=9)).isoformat(),
        "updated": (NOW - timedelta(minutes=55)).isoformat(),
        "description": "Stabilize webhook flows and validate checkout retries.",
    },
    {
        "key": "KAN-10",
        "title": "Bug Fix Search Bar",
        "summary": "Fix broken search in Jira workspace.",
        "status": "In Review",
        "priority": "High",
        "assignee": "Nora",
        "type": "Bug",
        "labels": ["frontend", "search"],
        "created": (NOW - timedelta(days=3)).isoformat(),
        "updated": (NOW - timedelta(minutes=35)).isoformat(),
        "description": "Search needs debounce and empty state handling.",
    },
    {
        "key": "KAN-1",
        "title": "Login Page UI",
        "summary": "Deliver responsive login form.",
        "status": "Done",
        "priority": "Medium",
        "assignee": "Mahdi",
        "type": "Task",
        "labels": ["frontend", "auth"],
        "created": (NOW - timedelta(days=12)).isoformat(),
        "updated": (NOW - timedelta(days=1)).isoformat(),
        "description": "Completed mobile and desktop login variants.",
    },
    {
        "key": "KAN-4",
        "title": "Navbar Responsive Fix",
        "summary": "Improve collapsible nav behavior.",
        "status": "Done",
        "priority": "Low",
        "assignee": "Yousef",
        "type": "Task",
        "labels": ["frontend", "ux"],
        "created": (NOW - timedelta(days=10)).isoformat(),
        "updated": (NOW - timedelta(days=2)).isoformat(),
        "description": "Sidebar and mobile nav polish completed.",
    },
    {
        "key": "KAN-8",
        "title": "Dark Mode UI",
        "summary": "Ship dark theme styles.",
        "status": "Done",
        "priority": "Medium",
        "assignee": "Lina",
        "type": "Story",
        "labels": ["frontend", "theme"],
        "created": (NOW - timedelta(days=11)).isoformat(),
        "updated": (NOW - timedelta(days=2)).isoformat(),
        "description": "Theme tokens and chart surfaces implemented.",
    },
]

PIPELINE_RUNS: List[Dict[str, Any]] = [
    {
        "id": "run-1042",
        "name": "KAN-2 registration pipeline",
        "status": "Running",
        "branch": "feature/user-registration",
        "commit": "a81c0e2",
        "startedAt": (NOW - timedelta(minutes=18)).isoformat(),
        "duration": "18m",
        "trigger": "Jira ticket",
        "ticketKey": "KAN-2",
        "failedTests": 1,
        "artifacts": ["coverage.xml", "pytest.log"],
        "steps": [
            {"name": "Checkout", "status": "Completed", "duration": "20s"},
            {"name": "Install deps", "status": "Completed", "duration": "1m 10s"},
            {"name": "Unit tests", "status": "Running", "duration": "6m 15s"},
            {"name": "PR summary", "status": "Queued", "duration": "-"},
        ],
        "logs": [
            "[12:01:14] cloning repository",
            "[12:01:39] installing dependencies",
            "[12:03:10] running pytest -q",
            "[12:06:42] 1 test failed in backend/test_user_registration.py",
            "[12:07:05] AI review agent preparing fix suggestion",
        ],
        "testResults": [
            {"name": "test_successful_user_registration", "status": "passed"},
            {"name": "test_duplicate_email_registration", "status": "passed"},
            {"name": "test_invalid_email_format", "status": "failed"},
        ],
    },
    {
        "id": "run-1041",
        "name": "Main branch verification",
        "status": "Failed",
        "branch": "main",
        "commit": "14db7ef",
        "startedAt": (NOW - timedelta(hours=2, minutes=12)).isoformat(),
        "duration": "11m",
        "trigger": "GitHub push",
        "ticketKey": "KAN-10",
        "failedTests": 3,
        "artifacts": ["failed-jobs.json", "screenshots.zip"],
        "steps": [
            {"name": "Checkout", "status": "Completed", "duration": "18s"},
            {"name": "Lint", "status": "Completed", "duration": "2m 05s"},
            {"name": "Playwright", "status": "Failed", "duration": "4m 44s"},
        ],
        "logs": [
            "[09:44:10] starting workflow frontend-tests.yml",
            "[09:48:51] search bar e2e assertion failed",
            "[09:49:02] screenshot uploaded to artifacts",
        ],
        "testResults": [
            {"name": "search-input opens result list", "status": "failed"},
            {"name": "search empty state renders", "status": "failed"},
            {"name": "dashboard cards count", "status": "failed"},
        ],
    },
    {
        "id": "run-1040",
        "name": "Dark mode release smoke",
        "status": "Succeeded",
        "branch": "release/ui-theme",
        "commit": "77ce211",
        "startedAt": (NOW - timedelta(hours=5)).isoformat(),
        "duration": "8m",
        "trigger": "Manual",
        "ticketKey": "KAN-8",
        "failedTests": 0,
        "artifacts": ["build.zip"],
        "steps": [
            {"name": "Checkout", "status": "Completed", "duration": "15s"},
            {"name": "Build", "status": "Completed", "duration": "3m 02s"},
            {"name": "Smoke tests", "status": "Completed", "duration": "2m 41s"},
        ],
        "logs": ["[06:12:10] release pipeline started", "[06:20:18] smoke tests passed"],
        "testResults": [
            {"name": "theme toggles persist", "status": "passed"},
            {"name": "dashboard charts render", "status": "passed"},
        ],
    },
]

PULL_REQUESTS: List[Dict[str, Any]] = [
    {
        "id": 212,
        "title": "feat: build Jira workspace and dashboard analytics",
        "repository": "mahdi20202/AI-DevOps-Pipeline",
        "author": "Mahdi",
        "status": "Open",
        "reviewStatus": "Changes requested",
        "branch": "feature/jira-dashboard",
        "additions": 428,
        "deletions": 76,
        "summary": "Adds KPI cards, charts, issue table, and Jira sync controls.",
        "diffOverview": ["Dashboard page scaffolded", "Shared stat cards added", "Jira board filters connected"],
    },
    {
        "id": 213,
        "title": "fix: stabilize user registration validation",
        "repository": "mahdi20202/AI-DevOps-Pipeline",
        "author": "AI Review Agent",
        "status": "Open",
        "reviewStatus": "Awaiting review",
        "branch": "ai/fix-registration-validation",
        "additions": 89,
        "deletions": 12,
        "summary": "Repairs invalid email and duplicate user edge cases from failed tests.",
        "diffOverview": ["Validation tightened", "Tests extended", "Error messages aligned"],
    },
    {
        "id": 208,
        "title": "chore: dark mode polish",
        "repository": "mahdi20202/AI-DevOps-Pipeline",
        "author": "Lina",
        "status": "Merged",
        "reviewStatus": "Approved",
        "branch": "release/ui-theme",
        "additions": 164,
        "deletions": 23,
        "summary": "Final theme token cleanup before release.",
        "diffOverview": ["Theme tokens refined", "Chart contrast improved"],
    },
]

GITHUB_DATA: Dict[str, Any] = {
    "repositories": [
        {"name": "AI-DevOps-Pipeline", "private": False, "defaultBranch": "main", "stars": 0, "openPrs": 2},
        {"name": "platform-shared-ui", "private": True, "defaultBranch": "main", "stars": 12, "openPrs": 4},
    ],
    "branches": [
        {"name": "main", "lastCommit": "14db7ef", "status": "Protected"},
        {"name": "feature/jira-dashboard", "lastCommit": "a81c0e2", "status": "Active"},
        {"name": "ai/fix-registration-validation", "lastCommit": "c21098b", "status": "Active"},
    ],
    "commits": [
        {"sha": "a81c0e2", "message": "feat: add Jira workspace widgets", "author": "Mahdi", "time": "18m ago"},
        {"sha": "c21098b", "message": "fix: align registration errors", "author": "AI Review Agent", "time": "42m ago"},
        {"sha": "14db7ef", "message": "test: improve dashboard assertions", "author": "Nora", "time": "2h ago"},
    ],
}

AGENT_ACTIVITY = [
    {"agent": "Planner Agent", "action": "Mapped KAN-2 into backend and test tasks", "time": "22m ago", "status": "completed"},
    {"agent": "Review Agent", "action": "Explained failing registration assertion", "time": "17m ago", "status": "running"},
    {"agent": "PR Agent", "action": "Generated summary for PR #213", "time": "58m ago", "status": "completed"},
    {"agent": "RAG Agent", "action": "Retrieved architecture_notes.md for AI Assistant answer", "time": "1h ago", "status": "completed"},
]

ACTION_RUNS = [
    {"name": "frontend-tests.yml", "status": "Failed", "failedJobs": 2, "retryUrl": "#/actions/frontend-tests"},
    {"name": "backend-tests.yml", "status": "Running", "failedJobs": 0, "retryUrl": "#/actions/backend-tests"},
    {"name": "docker-build.yml", "status": "Succeeded", "failedJobs": 0, "retryUrl": "#/actions/docker-build"},
]

REPORTS = {
    "passFailTrends": [
        {"label": "Mon", "passed": 18, "failed": 3},
        {"label": "Tue", "passed": 21, "failed": 4},
        {"label": "Wed", "passed": 23, "failed": 2},
        {"label": "Thu", "passed": 19, "failed": 5},
        {"label": "Fri", "passed": 24, "failed": 1},
    ],
    "agentSuccessRate": [
        {"name": "Planner", "value": 96},
        {"name": "Code", "value": 89},
        {"name": "Test", "value": 92},
        {"name": "Review", "value": 84},
    ],
    "jiraCycleTime": [
        {"name": "To Do", "days": 2.4},
        {"name": "In Progress", "days": 3.2},
        {"name": "In Review", "days": 1.4},
        {"name": "Done", "days": 4.8},
    ],
    "prThroughput": [
        {"label": "Week 1", "value": 6},
        {"label": "Week 2", "value": 9},
        {"label": "Week 3", "value": 7},
        {"label": "Week 4", "value": 11},
    ],
}

SETTINGS = {
    "jira": {"baseUrl": "https://your-domain.atlassian.net", "projectKey": "KAN", "email": "mahdi@example.com", "connected": True},
    "github": {"provider": "GitHub OAuth", "repo": "mahdi20202/AI-DevOps-Pipeline", "connected": True},
    "llm": {"provider": "Gemini 2.5 Flash", "temperature": 0.2, "connected": True},
    "vectorDb": {"provider": "FAISS", "embeddingModel": "text-embedding-3-small", "connected": True},
}


class AskPayload(BaseModel):
    question: str


class TicketPayload(BaseModel):
    title: str
    description: str = ""
    priority: str = "Medium"
    assignee: str = "Unassigned"
    type: str = "Task"


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "AI DevOps Platform API is running"}


@app.get("/api/dashboard")
def dashboard() -> Dict[str, Any]:
    active_runs = sum(1 for run in PIPELINE_RUNS if run["status"] == "Running")
    failed_tests = sum(run["failedTests"] for run in PIPELINE_RUNS)
    open_prs = sum(1 for pr in PULL_REQUESTS if pr["status"] == "Open")
    metrics = {
        "totalTickets": len(JIRA_TICKETS),
        "activePipelineRuns": active_runs,
        "failedTests": failed_tests,
        "openPrs": open_prs,
        "recentAgentActivity": len(AGENT_ACTIVITY),
    }
    return {
        "metrics": metrics,
        "tickets": JIRA_TICKETS,
        "pipelineRuns": PIPELINE_RUNS,
        "pullRequests": PULL_REQUESTS,
        "agentActivity": AGENT_ACTIVITY,
    }


@app.get("/api/jira")
def get_jira() -> Dict[str, Any]:
    return {"tickets": JIRA_TICKETS}


@app.get("/api/jira/{ticket_key}")
def get_jira_ticket(ticket_key: str) -> Dict[str, Any]:
    for ticket in JIRA_TICKETS:
        if ticket["key"] == ticket_key.upper():
            return ticket
    return {"message": "Ticket not found", "key": ticket_key.upper()}


@app.post("/api/jira/tickets")
def create_ticket(payload: TicketPayload) -> Dict[str, Any]:
    next_number = len(JIRA_TICKETS) + 1
    ticket = {
        "key": f"KAN-{next_number}",
        "title": payload.title,
        "summary": payload.title,
        "status": "To Do",
        "priority": payload.priority,
        "assignee": payload.assignee,
        "type": payload.type,
        "labels": ["created-from-ui"],
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat(),
        "description": payload.description,
    }
    JIRA_TICKETS.insert(0, ticket)
    return {"message": "Ticket created", "ticket": ticket}


@app.post("/api/jira/{ticket_key}/sync")
def sync_ticket(ticket_key: str) -> Dict[str, str]:
    return {"message": f"Sync completed for {ticket_key.upper()}"}


@app.post("/api/jira/{ticket_key}/trigger-pipeline")
def trigger_pipeline(ticket_key: str) -> Dict[str, Any]:
    run = {
        "id": f"run-{1042 + len(PIPELINE_RUNS)}",
        "name": f"{ticket_key.upper()} generated pipeline",
        "status": "Running",
        "branch": f"ticket/{ticket_key.lower()}",
        "commit": "pending",
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "duration": "0m",
        "trigger": "Jira ticket",
        "ticketKey": ticket_key.upper(),
        "failedTests": 0,
        "artifacts": [],
        "steps": [
            {"name": "Checkout", "status": "Queued", "duration": "-"},
            {"name": "Build", "status": "Queued", "duration": "-"},
        ],
        "logs": [f"[{datetime.now().strftime('%H:%M:%S')}] pipeline created from Jira workspace"],
        "testResults": [],
    }
    PIPELINE_RUNS.insert(0, run)
    return {"message": f"Pipeline started for {ticket_key.upper()}", "run": run}


@app.get("/api/github")
def get_github() -> Dict[str, Any]:
    return {
        **GITHUB_DATA,
        "pullRequests": PULL_REQUESTS,
        "workflowRuns": ACTION_RUNS,
    }


@app.get("/api/pipelines")
def get_pipelines() -> Dict[str, Any]:
    return {"runs": PIPELINE_RUNS}


@app.post("/api/pipelines/start")
def start_pipeline() -> Dict[str, Any]:
    return trigger_pipeline("KAN-3")


@app.get("/api/pull-requests")
def get_pull_requests() -> Dict[str, Any]:
    return {"pullRequests": PULL_REQUESTS}


@app.get("/api/actions")
def get_actions() -> Dict[str, Any]:
    return {"workflowRuns": ACTION_RUNS, "pipelineRuns": PIPELINE_RUNS}


@app.get("/api/reports")
def get_reports() -> Dict[str, Any]:
    return REPORTS


@app.get("/api/settings")
def get_settings() -> Dict[str, Any]:
    return SETTINGS


@app.post("/api/assistant/ask")
def ask_assistant(payload: AskPayload) -> Dict[str, Any]:
    question = payload.question.strip()
    lower_question = question.lower()
    if not question:
        return {"answer": "Please enter a project question."}
    if "pipeline" in lower_question:
        answer = "There are 3 pipeline runs, 1 is currently active, and the latest failure came from frontend search tests. Suggested next step: retry the failed job after applying the search bar fix."
    elif "pr" in lower_question or "pull request" in lower_question:
        answer = "There are 2 open pull requests. PR #212 needs changes, while PR #213 is waiting for review."
    elif "jira" in lower_question or "ticket" in lower_question:
        answer = "The Jira board has 10 tickets: 3 To Do, 2 In Progress, 2 In Review, and 3 Done. KAN-2 is the most active delivery item."
    elif "code" in lower_question or "fix" in lower_question:
        answer = "The registration flow likely needs stricter email validation alignment. Review backend.user_service and the duplicate email test before rerunning pytest."
    else:
        answer = "Based on the current project data, the platform is healthy overall, but pipeline quality is being dragged down by a small set of frontend failures and one active registration API issue."
    return {
        "question": question,
        "answer": answer,
        "sources": ["architecture_notes.md", "testing_requirements.md", "backend/test_user_registration.py"],
    }
