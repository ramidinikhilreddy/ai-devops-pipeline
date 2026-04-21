import json


def build_analyzer_prompt(current_code: str, pytest_output: str) -> str:
    return f"""
You are a FastAPI debugging agent.

Your task is to analyze failing code using these FIXED project rules.

PROJECT RULES (must not be changed):
- endpoint must be POST /register
- name must not be empty
- email must be valid using EmailStr
- password minimum length must be 8
- invalid input must return 422
- successful registration must return 201
- success response must be exactly:
{{
  "message": "User registered successfully",
  "registered_user": {{
    "name": "user.name",
    "email": "user.email"
  }}
}}

CRITICAL:
- Focus only on issues that prevent tests from passing
- Do NOT suggest alternative requirements
- Do NOT invent new thresholds
- Do NOT discuss security, best practices, or enhancements unless directly required
- Return ONLY valid JSON
- Keep output short and structured

Return JSON in exactly this format:
{{
  "issues": [
    "..."
  ],
  "fix_plan": [
    "..."
  ]
}}

Code:
{current_code}

Pytest Output:
{pytest_output}
""".strip()


def build_fixer_prompt(current_code: str, analysis: dict, pytest_output: str) -> str:
    return f"""
You are a senior Python backend engineer.

Fix the FastAPI application so that ALL tests pass.

PROJECT RULES (must be followed exactly):
- endpoint must be POST /register
- app variable name must be exactly: app
- name must not be empty -> 422
- email must be valid using EmailStr -> 422
- password minimum length must be 8 -> 422
- successful registration must return HTTP 201
- response body must be exactly:
{{
    "message": "User registered successfully",
    "registered_user": {{
        "name": user.name,
        "email": user.email
    }}
}}

CRITICAL OUTPUT RULES:
- Return ONE complete Python file
- Return the full file from first import to last line
- Do NOT return a patch
- Do NOT return a diff
- Do NOT return partial code
- Do NOT return markdown
- Do NOT return explanation
- Output only raw Python code

Analysis:
{json.dumps(analysis, indent=2)}

Current Code:
{current_code}

Pytest Output:
{pytest_output}

Rewrite the COMPLETE corrected file now.
""".strip()