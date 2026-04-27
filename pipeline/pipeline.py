from pathlib import Path
import ast
import difflib
import json
import time

from llm.llm_service import LLMService
from llm.agents import run_analyzer_agent, run_fixer_agent
from pipeline.ci_runner import run_pytest
from jira.fetch_ticket import fetch_jira_ticket
from pipeline.pr_summary import generate_pr_summary

APP_FILE = Path("project/app.py")
RAW_OUTPUT_FILE = Path("project/llm_last_output.py")
BACKUP_FILE = Path("project/app_before_fix.py")
METRICS_FILE = Path("project/pipeline_metrics.json")


def save_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def is_valid_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        print(f"❌ Generated code has syntax error: {e}")
        return False


def looks_like_complete_fastapi_app(code: str) -> bool:
    required_markers = [
        "from fastapi import",
        "FastAPI",
        "app = FastAPI(",
        '@app.post("/register"',
    ]
    return all(marker in code for marker in required_markers)


def print_diff(before: str, after: str) -> None:
    diff = difflib.unified_diff(
        before.splitlines(),
        after.splitlines(),
        fromfile="before",
        tofile="after",
        lineterm=""
    )

    print("\n===== CHANGE DIFF =====\n")
    found_changes = False

    for line in diff:
        if line.startswith(("---", "+++", "@@")):
            continue
        if line.startswith("-") or line.startswith("+"):
            print(line)
            found_changes = True

    if not found_changes:
        print("No visible code changes found.")


def print_generation_summary(before_code: str, generated_code: str) -> None:
    before_lines = len(before_code.splitlines())
    after_lines = len(generated_code.splitlines())
    lines = generated_code.splitlines()

    print("\n===== LLM OUTPUT CHECK =====\n")
    print(f"Original file lines : {before_lines}")
    print(f"Generated file lines: {after_lines}")
    print(f"Saved raw LLM output: {RAW_OUTPUT_FILE}")

    print("\nStructure check:")
    print(f"- Valid Python: {'YES' if is_valid_python(generated_code) else 'NO'}")
    print(
        f"- Looks like complete FastAPI file: "
        f"{'YES' if looks_like_complete_fastapi_app(generated_code) else 'NO'}"
    )

    print("\nQuick output preview:")
    print(f"- First line: {lines[0] if lines else 'EMPTY'}")
    print(f"- Last line : {lines[-1] if lines else 'EMPTY'}")


def load_jira_ticket() -> str:
    try:
        ticket = fetch_jira_ticket()
        print("\n📄 JIRA TICKET FETCHED SUCCESSFULLY\n")
        print(ticket)
        return ticket
    except Exception as e:
        print(f"\n⚠️ Jira ticket fetch failed: {e}")
        print("Continuing without Jira ticket context.\n")
        return ""


def save_metrics(passed: bool, retries_used: int, duration_seconds: float) -> None:
    metrics = {
        "passed": passed,
        "retries": retries_used,
        "with_rag": True,
        "duration_seconds": round(duration_seconds, 2),
    }
    save_file(METRICS_FILE, json.dumps(metrics, indent=2))


def run_pipeline() -> None:
    start_time = time.time()
    llm = LLMService()

    if not APP_FILE.exists():
        print(f"❌ File not found: {APP_FILE}")
        return

    print("\n===== PIPELINE FLOW =====\n")

    jira_ticket = load_jira_ticket()

    before_code = APP_FILE.read_text(encoding="utf-8")
    save_file(BACKUP_FILE, before_code)

    result = run_pytest()
    retries_used = 0
    final_pytest_output = result.stdout

    if result.returncode == 0:
        print("Attempt 1: PASS ✅")

        save_metrics(
            passed=True,
            retries_used=0,
            duration_seconds=time.time() - start_time,
        )

        if llm.available:
            summary = generate_pr_summary(
                llm=llm,
                jira_ticket=jira_ticket,
                pytest_output=final_pytest_output,
                test_passed=True,
                retries_used=0,
            )
            if summary:
                print("\n===== PR SUMMARY =====\n")
                print(summary)

        print("\n===== SUMMARY =====\n")
        print("Final Result: PASS ✅")
        print("Code already satisfies tests.")
        print("\nPipeline completed 🚀")
        return

    print("Attempt 1: FAIL ❌")
    print("\n❌ Reason:")
    print("Initial test run failed. Starting multi-agent repair flow.\n")

    if not llm.available:
        print("⚠️ Real LLM is disabled or unavailable.")
        print("No repair attempt will be made.")
        save_metrics(
            passed=False,
            retries_used=0,
            duration_seconds=time.time() - start_time,
        )
        print("\n===== SUMMARY =====\n")
        print("Final Result: FAIL ❌")
        print("Reason: LLM unavailable.")
        return

    analysis = run_analyzer_agent(
        llm=llm,
        current_code=before_code,
        pytest_output=result.stdout + (f"\n\nJIRA TICKET:\n{jira_ticket}" if jira_ticket else "")
    )

    if not analysis:
        save_metrics(
            passed=False,
            retries_used=0,
            duration_seconds=time.time() - start_time,
        )
        print("❌ Analyzer failed — stopping")
        print("\n===== SUMMARY =====\n")
        print("Final Result: FAIL ❌")
        print("Reason: Analyzer agent returned no usable output.")
        return

    print("Analyzer Output:")
    print(analysis)

    fixed_code = run_fixer_agent(
        llm=llm,
        current_code=before_code,
        analysis=analysis,
        pytest_output=result.stdout + (f"\n\nJIRA TICKET:\n{jira_ticket}" if jira_ticket else "")
    )

    if not fixed_code.strip():
        save_metrics(
            passed=False,
            retries_used=0,
            duration_seconds=time.time() - start_time,
        )
        print("❌ Fixer failed — stopping")
        print("\n===== SUMMARY =====\n")
        print("Final Result: FAIL ❌")
        print("Reason: Fixer agent returned no usable output.")
        return

    save_file(RAW_OUTPUT_FILE, fixed_code)
    print_generation_summary(before_code, fixed_code)

    if not is_valid_python(fixed_code):
        save_metrics(
            passed=False,
            retries_used=0,
            duration_seconds=time.time() - start_time,
        )
        print("❌ Invalid Python generated — stopping")
        print("\n===== SUMMARY =====\n")
        print("Final Result: FAIL ❌")
        print("Reason: Generated code had syntax errors.")
        return

    if not looks_like_complete_fastapi_app(fixed_code):
        save_metrics(
            passed=False,
            retries_used=0,
            duration_seconds=time.time() - start_time,
        )
        print("❌ Incomplete FastAPI app generated — stopping")
        print("\n===== SUMMARY =====\n")
        print("Final Result: FAIL ❌")
        print("Reason: Generated code did not look like a complete FastAPI file.")
        return

    save_file(APP_FILE, fixed_code)

    after_code = APP_FILE.read_text(encoding="utf-8")
    print_diff(before_code, after_code)

    print("\n👉 Updated app.py with full LLM output")
    print(f"👉 Backup saved at: {BACKUP_FILE}")
    print(f"👉 Raw generated file saved at: {RAW_OUTPUT_FILE}\n")

    result = run_pytest()
    retries_used = 1
    final_pytest_output = result.stdout
    test_passed = result.returncode == 0

    save_metrics(
        passed=test_passed,
        retries_used=retries_used,
        duration_seconds=time.time() - start_time,
    )

    summary = generate_pr_summary(
        llm=llm,
        jira_ticket=jira_ticket,
        pytest_output=final_pytest_output,
        test_passed=test_passed,
        retries_used=retries_used,
    )
    if summary:
        print("\n===== PR SUMMARY =====\n")
        print(summary)

    if test_passed:
        print("Attempt 2: PASS ✅")
        print("\n===== SUMMARY =====\n")
        print("Final Result: PASS ✅")
        print("Multi-agent LLM output was accepted as a full FastAPI file.")
        print("\nPipeline completed 🚀")
    else:
        print("Attempt 2: FAIL ❌")
        print("\n===== SUMMARY =====\n")
        print("Final Result: FAIL ❌")
        print("Reason: Tests still failed after multi-agent fix.")


if __name__ == "__main__":
    run_pipeline()