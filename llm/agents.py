import json

from llm.prompts import (
    build_analyzer_prompt,
    build_fixer_prompt,
    build_pr_summary_prompt,
)


def run_analyzer_agent(llm, current_code: str, pytest_output: str) -> dict:
    print("\n🧠 Analyzer Agent running...\n")

    prompt = build_analyzer_prompt(current_code, pytest_output)
    response = llm.generate(prompt)

    if not response.strip():
        print("❌ Analyzer returned empty output")
        return {}

    try:
        parsed = json.loads(response)
        print("✅ Analyzer output parsed successfully\n")
        return parsed
    except Exception as e:
        print("❌ Failed to parse analyzer output:", e)
        print("Raw response:\n", response)
        return {}


def run_fixer_agent(llm, current_code: str, analysis: dict, pytest_output: str) -> str:
    print("\n🔧 Fixer Agent running...\n")

    prompt = build_fixer_prompt(current_code, analysis, pytest_output)
    response = llm.generate(prompt)

    if not response.strip():
        print("❌ Fixer returned empty output")
        return ""

    print("✅ Fixer generated code\n")
    return response


def run_pr_summary_agent(
    llm,
    jira_ticket: str,
    changed_files: list[str],
    diff_text: str,
    pytest_output: str,
    test_passed: bool,
    retries_used: int,
) -> str:
    print("\n📝 PR Summary Agent running...\n")

    prompt = build_pr_summary_prompt(
        jira_ticket=jira_ticket,
        changed_files=changed_files,
        diff_text=diff_text,
        pytest_output=pytest_output,
        test_passed=test_passed,
        retries_used=retries_used,
    )

    response = llm.generate(prompt)

    if not response.strip():
        print("❌ PR Summary Agent returned empty output")
        return ""

    print("✅ PR Summary generated\n")
    return response