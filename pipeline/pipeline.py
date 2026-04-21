from pathlib import Path
import ast
import difflib

from llm.llm_service import LLMService
from llm.agents import run_analyzer_agent, run_fixer_agent
from pipeline.ci_runner import run_pytest

APP_FILE = Path("project/app.py")


def save_file(path, content):
    path.write_text(content, encoding="utf-8")


def is_valid_python(code: str):
    try:
        ast.parse(code)
        return True
    except Exception as e:
        print("❌ Syntax error:", e)
        return False


def print_diff(before, after):
    diff = difflib.unified_diff(
        before.splitlines(),
        after.splitlines(),
        lineterm=""
    )

    print("\n===== CHANGE DIFF =====\n")
    for line in diff:
        if line.startswith("-") or line.startswith("+"):
            print(line)


def run_pipeline():
    llm = LLMService()

    if not APP_FILE.exists():
        print("❌ app.py not found")
        return

    before_code = APP_FILE.read_text()

    print("\n===== PIPELINE FLOW =====\n")

    result = run_pytest()

    if result.returncode == 0:
        print("Attempt 1: PASS ✅")
        return

    print("Attempt 1: FAIL ❌")

    if not llm.available:
        print("❌ LLM disabled — stopping")
        return

    # 🧠 Step 1: Analyzer
    analysis = run_analyzer_agent(
        llm,
        current_code=before_code,
        pytest_output=result.stdout
    )

    if not analysis:
        print("❌ Analyzer failed — stopping")
        return

    print("Analyzer Output:")
    print(analysis)

    # 🔧 Step 2: Fixer
    fixed_code = run_fixer_agent(
        llm,
        current_code=before_code,
        analysis=analysis,
        pytest_output=result.stdout
    )

    if not fixed_code:
        print("❌ Fixer failed — stopping")
        return

    if not is_valid_python(fixed_code):
        print("❌ Invalid Python — stopping")
        return

    save_file(APP_FILE, fixed_code)

    after_code = APP_FILE.read_text()
    print_diff(before_code, after_code)

    # 🔁 Run again
    result = run_pytest()

    if result.returncode == 0:
        print("\nAttempt 2: PASS ✅")
    else:
        print("\nAttempt 2: FAIL ❌")


if __name__ == "__main__":
    run_pipeline()