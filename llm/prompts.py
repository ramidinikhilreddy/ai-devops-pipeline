import json


def build_requirement_prompt(ticket_text: str) -> str:
    return f"""
Convert the following software requirement into structured JSON.

Return ONLY valid JSON.
No markdown. No explanation.

Schema:
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

Generate ONLY valid Python FastAPI code.

STRICT RULES:
- No markdown
- No explanation
- Single file
- Use FastAPI
- Endpoint: POST /register
- Use Pydantic
- Validate:
    - name must not be empty
    - email must be valid
    - password min length = 8

RESPONSE FORMAT (VERY IMPORTANT):
return {{
    "message": "User registered successfully",
    "registered_user": {{
        "name": user.name,
        "email": user.email
    }}
}}

Requirement:
{requirement_text}
"""


def build_fix_prompt(requirement_json: dict, current_code: str, pytest_output: str) -> str:
    requirement_text = json.dumps(requirement_json, indent=2)

    return f"""
You are a senior Python backend engineer.

Your task: FIX the FastAPI code so ALL pytest tests PASS.

STRICT RULES:
- Return ONLY Python code
- No markdown
- No explanation
- Keep FastAPI app name = app
- Endpoint must be /register

CRITICAL:
Response MUST be EXACTLY:

{{
    "message": "User registered successfully",
    "registered_user": {{
        "name": user.name,
        "email": user.email
    }}
}}

VALIDATION RULES:
- name must not be empty → return 422
- email must be valid → return 422
- password min length = 8 → return 422

Requirement:
{requirement_text}

Current Code:
{current_code}

Pytest Output:
{pytest_output}

Fix ALL issues so tests pass.
"""