import json
import os
import subprocess
import sys

from llm.llm_service import LLMService
from llm.prompts import build_requirement_prompt, build_code_prompt, build_fix_prompt

# ✅ RAG import
from rag.retriever import retrieve_context

USE_REAL_LLM = False   # set False if quota issue
MAX_FIX_ATTEMPTS = 2


def ensure_directories():
    os.makedirs("project", exist_ok=True)
    os.makedirs("project/tests", exist_ok=True)


def save_file(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)


def run_pytest():
    print("\nRUNNING PYTEST...\n")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "project/tests/test_app.py", "-v"],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode == 0:
        print("\nALL TESTS PASSED ✅")
    else:
        print("\nTESTS FAILED ❌")

    return result.returncode, result.stdout


def main():
    ensure_directories()

    llm = LLMService()

    # 🎯 STEP 1: USER REQUIREMENT
    ticket = """
    Create an API endpoint to register a user with name, email, and password.
    Email must be valid. Password must be at least 8 characters.
    """

    # 🔥 STEP 2: GET RAG CONTEXT
    context = retrieve_context(ticket, top_k=3)

    print("\n===== RAG CONTEXT =====\n")
    print(context)

    # 🔥 STEP 3: COMBINE CONTEXT + REQUIREMENT
    enhanced_ticket = f"""
    Context:
    {context}

    Requirement:
    {ticket}
    """

    # 🔥 STEP 4: GENERATE REQUIREMENT JSON
    requirement_prompt = build_requirement_prompt(enhanced_ticket)
    requirement_json = json.loads(llm.generate(requirement_prompt))

    print("\nREQUIREMENT JSON:\n")
    print(json.dumps(requirement_json, indent=2))

    save_file("project/requirement.json", json.dumps(requirement_json, indent=2))

    # 🔥 STEP 5: GENERATE CODE
    code_prompt = build_code_prompt(requirement_json)
    code = llm.generate(code_prompt)

    # ❗ OPTIONAL: force failure for demo
    code = code.replace("min_length=8", "min_length=2")

    save_file("project/app.py", code)
    print("\nCode saved to project/app.py")

    # 🔥 STEP 6: TEST FILE
    tests = """
from fastapi.testclient import TestClient
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

def test_missing_name():
    response = client.post("/register", json={
        "name": "",
        "email": "test@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 422
"""

    save_file("project/tests/test_app.py", tests)
    print("\nTests saved to project/tests/test_app.py")

    # 🔁 STEP 7: AUTO-FIX LOOP
    for attempt in range(MAX_FIX_ATTEMPTS + 1):
        print(f"\n=== TEST ATTEMPT {attempt + 1} ===")

        returncode, output = run_pytest()

        if returncode == 0:
            print("\nPipeline completed successfully ✅")
            break

        print("\nTrying LLM-based auto-fix...")

        current_code = open("project/app.py").read()

        fix_prompt = build_fix_prompt(requirement_json, current_code, output)
        fixed_code = llm.generate(fix_prompt)

        save_file("project/app.py", fixed_code)
        print("\nFixed code written to project/app.py")


if __name__ == "__main__":
    main()