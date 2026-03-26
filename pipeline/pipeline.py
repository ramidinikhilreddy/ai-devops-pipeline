from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from llm.llm_service import LLMService
from llm.prompts import build_code_prompt, build_fix_prompt, build_requirement_prompt
from pipeline.ci_runner import run_pytest
from pipeline.evaluation import MetricsTracker
from pipeline.git_utils import get_git_status, write_demo_summary
from rag.retriever import retrieve_context

MAX_FIX_ATTEMPTS = 2


# ---------------- MOCK FIXER ----------------

class MockFixer:
    @staticmethod
    def fix_app_code(current_code: str) -> str:
        """
        Simulates AI fixing logic when LLM is OFF.
        """

        # Fix password validation
        current_code = current_code.replace("min_length=2", "min_length=8")

        # Fix status code
        current_code = current_code.replace("status_code=200", "status_code=201")

        # Fix response structure
        if '"registered_user"' not in current_code:
            current_code = current_code.replace(
                'return {"message": "User registered successfully"}',
                'return {"message": "User registered successfully", "registered_user": {"name": user.name, "email": user.email}}'
            )

        return current_code


# ---------------- DATA ----------------

MOCK_REQUIREMENT = {
    "feature_name": "User Registration API",
    "description": "Create an API endpoint to register a user with name, email, and password.",
}

BROKEN_APP_CODE = '''from fastapi import FastAPI, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

class UserRegister(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=2)

@app.post("/register", status_code=200)
def register_user(user: UserRegister):
    return {"message": "User registered successfully"}
'''

TEST_CODE = '''from fastapi.testclient import TestClient
from project.app import app

client = TestClient(app)

def test_successful_registration():
    response = client.post("/register", json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 201

def test_invalid_email_format():
    response = client.post("/register", json={
        "name": "Jane",
        "email": "invalid",
        "password": "strongpassword123"
    })
    assert response.status_code == 422

def test_password_too_short():
    response = client.post("/register", json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "short"
    })
    assert response.status_code == 422
'''


# ---------------- HELPERS ----------------

def save_file(path: str, content: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")


# ---------------- PIPELINE ----------------

def run_pipeline(use_real_llm: bool = False, with_rag: bool = True):
    llm = LLMService() if use_real_llm else None
    tracker = MetricsTracker()

    # Step 1: Requirement
    ticket = "Create an API endpoint for user registration"

    # Step 2: RAG
    retrieved_context = retrieve_context(ticket, top_k=3) if with_rag else []

    # Step 3: Generate requirement + code
    if use_real_llm and llm and llm.available:
        prompt = build_requirement_prompt(ticket)
        requirement = json.loads(llm.generate(prompt))

        code_prompt = build_code_prompt(requirement)
        code = llm.generate(code_prompt)
    else:
        requirement = MOCK_REQUIREMENT
        code = BROKEN_APP_CODE

    save_file("project/requirement.json", json.dumps(requirement, indent=2))
    save_file("project/app.py", code)
    save_file("project/tests/test_app.py", TEST_CODE)

    # Step 4: Test + Fix loop
    retries = 0
    history = []

    result = run_pytest()
    history.append(result.to_dict())

    while result.returncode != 0 and retries < MAX_FIX_ATTEMPTS:
        retries += 1

        current_code = Path("project/app.py").read_text()

        if use_real_llm and llm and llm.available:
            fix_prompt = build_fix_prompt(requirement, current_code, result.stdout)
            fixed_code = llm.generate(fix_prompt)
        else:
            fixed_code = MockFixer.fix_app_code(current_code)

        save_file("project/app.py", fixed_code)

        result = run_pytest()
        history.append(result.to_dict())

    # Step 5: Metrics
    metrics = tracker.build_metrics(
        passed=result.returncode == 0,
        retries=retries,
        with_rag=with_rag,
        extra={"attempts": history, "context_chunks": len(retrieved_context)},
    )
    tracker.save(metrics)

    return {
        "requirement": requirement,
        "retrieved_context": retrieved_context,
        "test_result": result.to_dict(),
        "metrics": metrics,
    }


# ---------------- MAIN ----------------

if __name__ == "__main__":
    result = run_pipeline(use_real_llm=True, with_rag=True)

    print("\n===== PIPELINE FLOW =====\n")

    for i, attempt in enumerate(result["metrics"]["attempts"]):
        status = "PASS ✅" if attempt["returncode"] == 0 else "FAIL ❌"
        print(f"Attempt {i+1}: {status}")

    print("\n===== SUMMARY =====\n")
    print("Feature:", result["requirement"]["feature_name"])
    print("Final Result:", "PASS ✅" if result["test_result"]["returncode"] == 0 else "FAIL ❌")
    print("Retries:", result["metrics"]["retries"])
    print("Risk Level:", result["metrics"]["risk"]["level"])
    print("RAG Context Used:", len(result["retrieved_context"]))

    print("\nPipeline completed successfully 🚀")