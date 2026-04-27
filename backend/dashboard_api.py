import os
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

load_dotenv()

router = APIRouter(prefix="/api", tags=["dashboard"])


def _extract_priority(issue: Dict[str, Any]) -> str:
    priority = issue["fields"].get("priority")
    if not priority:
        return "Medium"
    return priority.get("name", "Medium")


def _extract_assignee(issue: Dict[str, Any]) -> str:
    assignee = issue["fields"].get("assignee")
    if not assignee:
        return "Unassigned"
    return assignee.get("displayName", "Unassigned")


def _extract_status(issue: Dict[str, Any]) -> str:
    status = issue["fields"].get("status", {}).get("name", "To Do")
    status_map = {
        "To Do": "To Do",
        "Selected for Development": "To Do",
        "In Progress": "In Progress",
        "In Review": "In Review",
        "Done": "Done",
    }
    return status_map.get(status, status)


def _extract_type(issue: Dict[str, Any]) -> str:
    issue_type = issue["fields"].get("issuetype")
    if not issue_type:
        return "Task"
    return issue_type.get("name", "Task")


@router.get("/dashboard")
def get_dashboard_data() -> Dict[str, Any]:
    base_url = os.getenv("JIRA_BASE_URL")
    email = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")
    project_key = os.getenv("JIRA_PROJECT_KEY", "KAN")

    if not base_url or not email or not api_token:
        raise HTTPException(status_code=500, detail="Missing Jira environment variables")

    search_url = f"{base_url}/rest/api/3/search"
    params = {
        "jql": f"project={project_key} ORDER BY created DESC",
        "maxResults": 50,
        "fields": "summary,status,priority,assignee,issuetype,created,updated",
    }

    response = requests.get(
        search_url,
        params=params,
        auth=(email, api_token),
        headers={"Accept": "application/json"},
        timeout=30,
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Jira search failed: {response.text}",
        )

    data = response.json()
    issues = data.get("issues", [])

    tickets: List[Dict[str, Any]] = []
    for issue in issues:
        tickets.append(
            {
                "key": issue["key"],
                "title": issue["fields"].get("summary", ""),
                "status": _extract_status(issue),
                "priority": _extract_priority(issue),
                "assignee": _extract_assignee(issue),
                "type": _extract_type(issue),
                "created": issue["fields"].get("created"),
                "updated": issue["fields"].get("updated"),
            }
        )

    return {"tickets": tickets}