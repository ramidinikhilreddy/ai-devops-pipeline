import json
from llm.prompts import build_analyzer_prompt, build_fixer_prompt


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