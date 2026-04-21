def build_fix_prompt(current_code: str, pytest_output: str) -> str:
    return f"""
You are a senior Python backend engineer.

Task:
Repair the FastAPI application below so that all pytest tests pass.

Return:
- ONE complete corrected Python file
- From first import to final line
- Raw Python code only
- No markdown
- No explanation
- No diff
- No patch
- No partial snippets

Requirements:
- Use FastAPI
- App variable name must be exactly: app
- Endpoint must be: POST /register
- Use Pydantic validation
- name must not be empty -> 422
- email must be valid -> 422
- password minimum length must be 8 -> 422
- success status code must be 201

Success response body must be exactly:
{{
    "message": "User registered successfully",
    "registered_user": {{
        "name": user.name,
        "email": user.email
    }}
}}

Current code:
{current_code}

Pytest output:
{pytest_output}

Return the full corrected file now.
""".strip()