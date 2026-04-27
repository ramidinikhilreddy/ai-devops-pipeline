import os
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()


def _extract_description_text(description: Any) -> str:
    if not isinstance(description, dict):
        return ""

    parts: List[str] = []

    for block in description.get("content", []):
        for item in block.get("content", []):
            text = item.get("text", "")
            if text:
                parts.append(text)

    return " ".join(parts).strip()


def _extract_status(issue: Dict[str, Any]) -> str:
    return issue["fields"].get("status", {}).get("name", "Unknown")


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


def _extract_type(issue: Dict[str, Any]) -> str:
    issue_type = issue["fields"].get("issuetype")
    if not issue_type:
        return "Task"
    return issue_type.get("name", "Task")


def fetch_all_jira_tickets() -> List[Dict[str, Any]]:
    base_url = os.getenv("JIRA_BASE_URL")
    email = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")
    project_key = os.getenv("JIRA_PROJECT_KEY", "KAN")

    if not base_url:
        raise Exception("Missing JIRA_BASE_URL in .env")
    if not email:
        raise Exception("Missing JIRA_EMAIL in .env")
    if not api_token:
        raise Exception("Missing JIRA_API_TOKEN in .env")
    if not project_key:
        raise Exception("Missing JIRA_PROJECT_KEY in .env")

    url = f"{base_url}/rest/api/3/search"

    params = {
        "jql": f"project={project_key} ORDER BY created ASC",
        "maxResults": 100,
        "fields": "summary,description,status,priority,assignee,issuetype,created,updated",
    }

    response = requests.get(
        url,
        params=params,
        auth=(email, api_token),
        headers={"Accept": "application/json"},
        timeout=30,
    )

    if response.status_code != 200:
        raise Exception(f"Jira fetch failed: {response.text}")

    data = response.json()
    issues = data.get("issues", [])

    tickets: List[Dict[str, Any]] = []

    for issue in issues:
        fields = issue.get("fields", {})
        tickets.append(
            {
                "key": issue.get("key", ""),
                "summary": fields.get("summary", ""),
                "description": _extract_description_text(fields.get("description")),
                "status": _extract_status(issue),
                "priority": _extract_priority(issue),
                "assignee": _extract_assignee(issue),
                "type": _extract_type(issue),
                "created": fields.get("created"),
                "updated": fields.get("updated"),
            }
        )

    return tickets


def fetch_all_jira_tickets_as_text() -> str:
    tickets = fetch_all_jira_tickets()

    output_parts: List[str] = []

    for ticket in tickets:
        block = (
            f"Key: {ticket['key']}\n"
            f"Summary: {ticket['summary']}\n"
            f"Type: {ticket['type']}\n"
            f"Status: {ticket['status']}\n"
            f"Priority: {ticket['priority']}\n"
            f"Assignee: {ticket['assignee']}\n"
            f"Description: {ticket['description']}\n"
        )
        output_parts.append(block)

    return "\n---\n".join(output_parts)


if __name__ == "__main__":
    tickets = fetch_all_jira_tickets()
    for ticket in tickets:
        print(ticket)