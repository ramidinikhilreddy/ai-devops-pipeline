from pathlib import Path
import difflib
import ast

from llm.llm_service import LLMService
from llm.prompts import build_fix_prompt
from pipeline.ci_runner import run_pytest

APP_FILE = Path("project/app.py")
RAW_OUTPUT_FILE = Path("project/llm_last_output.py")
BACKUP_FILE = Path("project/app_before_fix.py")


def save_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def print_diff(before: str, after: str) -> None:
    diff = difflib.unified_diff(
        before.splitlines(),
        after.splitlines(),
        fromfile="before",
        tofile="after",
        lineterm="",
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


def count_lines(code: str) -> int:
    return len(code.splitlines())


def print_generation_summary(before_code: str, generated_code: str) -> None:
    lines = generated_code.splitlines()

    print("\n===== LLM OUTPUT CHECK =====\n")
    print(f"Original file lines : {count_lines(before_code)}")
    print(f"Generated file lines: {count_lines(generated_code)}")
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


def run_pipeline() -> None:
    llm = LLMService()

    if not llm.available:
        print("❌ Real LLM not available")
        return

    if not APP_FILE.exists():
        print(f"❌ File not found: {APP_FILE}")
        return

    print("\n===== PIPELINE FLOW =====\n")

    before_code = APP_FILE.read_text(encoding="utf-8")
    save_file(BACKUP_FILE, before_code)

    result = run_pytest()

    if result.returncode == 0:
        print("Attempt 1: PASS ✅")
        print("\n===== SUMMARY =====\n")
        print("Final Result: PASS ✅")
        print("Pipeline completed 🚀")
        return

    print("Attempt 1: FAIL ❌")
    print("\n❌ Reason:")
    print("Initial test run failed. Sending minimal repair context to real LLM.\n")

    prompt = build_fix_prompt(
        current_code=before_code,
        pytest_output=result.stdout,
    )

    print("🧠 Real LLM fixing the code...\n")
    fixed_code = llm.generate(prompt)

    if not fixed_code.strip():
        print("❌ Real LLM returned empty output. Keeping existing code.")
        print("\n===== SUMMARY =====\n")
        print("Final Result: FAIL ❌")
        print("Reason: Real LLM did not return usable code.")
        return

    save_file(RAW_OUTPUT_FILE, fixed_code)
    print_generation_summary(before_code, fixed_code)

    if not is_valid_python(fixed_code):
        print("❌ Real LLM returned invalid Python code. Keeping existing code.")
        print("\n===== SUMMARY =====\n")
        print("Final Result: FAIL ❌")
        print("Reason: Generated code had syntax errors.")
        return

    if not looks_like_complete_fastapi_app(fixed_code):
        print("❌ Real LLM did not return a complete FastAPI file. Keeping existing code.")
        print("\n===== SUMMARY =====\n")
        print("Final Result: FAIL ❌")
        print("Reason: Generated output looked incomplete.")
        return

    save_file(APP_FILE, fixed_code)

    after_code = APP_FILE.read_text(encoding="utf-8")
    print_diff(before_code, after_code)

    print("\n👉 Updated app.py with full real LLM output")
    print(f"👉 Backup saved at: {BACKUP_FILE}")
    print(f"👉 Raw generated file saved at: {RAW_OUTPUT_FILE}\n")

    result = run_pytest()

    if result.returncode == 0:
        print("Attempt 2: PASS ✅")
        print("\n===== SUMMARY =====\n")
        print("Final Result: PASS ✅")
        print("Real LLM output was accepted as a full FastAPI file.")
        print("\nPipeline completed 🚀")
    else:
        print("Attempt 2: FAIL ❌")
        print("\n===== SUMMARY =====\n")
        print("Final Result: FAIL ❌")
        print("Reason: Tests still failed after real LLM fix.")


if __name__ == "__main__":
    run_pipeline()