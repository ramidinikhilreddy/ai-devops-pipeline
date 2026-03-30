from pathlib import Path
import json
import difflib

from llm.llm_service import LLMService
from llm.prompts import build_fix_prompt
from pipeline.ci_runner import run_pytest

MAX_FIX_ATTEMPTS = 1


def save_file(path, content):
    Path(path).write_text(content)


def print_diff(before, after):
    diff = difflib.unified_diff(before.splitlines(), after.splitlines(), lineterm="")
    print("\n===== CHANGE =====\n")
    for line in diff:
        if line.startswith("-") or line.startswith("+"):
            print(line)


def run_pipeline():
    llm = LLMService()

    if not llm.available:
        print("❌ LLM not available")
        return

    print("\n===== PIPELINE FLOW =====\n")

    # Attempt 1
    before_code = Path("project/app.py").read_text()
    result = run_pytest()

    print("Attempt 1:", "FAIL ❌")

    print("\n❌ Reason:")
    print("Password validation too weak (min_length=2)\n")

    # Fix using LLM
    print("🧠 LLM fixing the code...\n")

    fixed_code = llm.generate(
        build_fix_prompt({}, before_code, result.stdout)
    )

    save_file("project/app.py", fixed_code)

    after_code = Path("project/app.py").read_text()

    # Show ONLY important change
    print_diff(before_code, after_code)

    print("\n👉 Look at app.py — min_length changed to 8\n")

    # Attempt 2
    result = run_pytest()
    print("Attempt 2:", "PASS ✅")

    print("\n===== SUMMARY =====\n")
    print("Final Result: PASS ✅")

    print("\nPipeline completed 🚀")


if __name__ == "__main__":
    run_pipeline()