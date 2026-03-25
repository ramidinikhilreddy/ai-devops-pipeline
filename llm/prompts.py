import json


def build_requirement_prompt(ticket_text: str) -> str:
    return f"""
Convert the following software requirement into structured JSON.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanation text.

Use this exact schema:
{{
  "feature_name": "",
  "description": "",
  "inputs": [],
  "validations": [],
  "expected_output": "",
  "test_cases": []
}}

Requirement:
\"\"\"
{ticket_text}
\"\"\"
"""


def build_code_prompt(requirement_json: dict) -> str:
    requirement_text = json.dumps(requirement_json, indent=2)

    return f"""
You are a Python backend developer.

Using the requirement JSON below, generate ONLY valid Python code.

Rules:
- Return only Python code
- Use FastAPI
- Create one POST endpoint
- The endpoint path must be /register
- Use Pydantic models
- Add validation for email and password length
- Return HTTP 201 for success
- Keep the code in a single file
- Include all required imports
- Make the code runnable
- The FastAPI app variable must be named app

Requirement JSON:
{requirement_text}
"""


def build_test_prompt(requirement_json: dict, generated_code: str) -> str:
    requirement_text = json.dumps(requirement_json, indent=2)

    return f"""
You are a Python QA engineer.

Using the requirement JSON and the FastAPI code below, generate ONLY valid pytest code.

Rules:
- Return only Python code
- Use pytest
- Use fastapi.testclient.TestClient
- Import the app using: from project.app import app
- Test the /register endpoint
- Include happy path and validation failure cases
- For invalid input, expect FastAPI/Pydantic validation behavior
- DO NOT assert exact full validation messages because they vary by version
- DO NOT assume tuple locations; validation loc is usually a list
- Prefer flexible assertions like checking status code, field name in detail.loc, and key message fragments
- Keep everything in a single file
- Include all required imports
- Make the tests runnable

Requirement JSON:
{requirement_text}

Generated FastAPI Code:
{generated_code}
"""