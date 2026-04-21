import os
import requests
from dotenv import load_dotenv

load_dotenv()


def fetch_jira_ticket():
    base_url = os.getenv("JIRA_BASE_URL")
    email = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")
    ticket_key = os.getenv("JIRA_TICKET_KEY")

    url = f"{base_url}/rest/api/3/issue/{ticket_key}"

    response = requests.get(
        url,
        auth=(email, api_token),
        headers={"Accept": "application/json"}
    )

    if response.status_code != 200:
        raise Exception(f"Jira fetch failed: {response.text}")

    data = response.json()

    summary = data["fields"]["summary"]
    description = data["fields"]["description"]

    text = ""

    if isinstance(description, dict):
        for block in description.get("content", []):
            for item in block.get("content", []):
                text += item.get("text", "") + " "

    return f"{summary}\n{text}"