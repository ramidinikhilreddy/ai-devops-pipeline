import json
import subprocess
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="AI DevOps Pipeline Dashboard",
    page_icon="🚀",
    layout="wide",
)

PROJECT_DIR = Path("project")
APP_FILE = PROJECT_DIR / "app.py"
BACKUP_FILE = PROJECT_DIR / "app_before_fix.py"
RAW_OUTPUT_FILE = PROJECT_DIR / "llm_last_output.py"
REQUIREMENT_FILE = PROJECT_DIR / "requirement.json"
METRICS_FILE = PROJECT_DIR / "pipeline_metrics.json"
PR_SUMMARY_FILE = PROJECT_DIR / "pr_summary.txt"


def run_command(command: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def reset_demo() -> tuple[int, str, str]:
    return run_command(["python", "scripts/reset_demo.py"])


def run_pipeline() -> tuple[int, str, str]:
    return run_command(["python", "-m", "pipeline.pipeline"])


def read_file(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def read_json(path: Path):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def extract_jira_block(logs: str) -> str:
    if not logs:
        return ""

    lines = logs.splitlines()
    capture = False
    collected = []

    for line in lines:
        if "JIRA TICKET FETCHED SUCCESSFULLY" in line:
            capture = True
            continue

        if capture:
            if "Attempt 1:" in line:
                break
            collected.append(line)

    return "\n".join([line for line in collected if line.strip()]).strip()


def extract_analyzer_block(logs: str) -> str:
    if not logs:
        return ""

    lines = logs.splitlines()
    capture = False
    collected = []

    for line in lines:
        if line.strip().startswith("Analyzer Output:"):
            capture = True
            continue

        if capture:
            if "Fixer Agent running" in line or "🔧 Fixer Agent running" in line:
                break
            collected.append(line)

    return "\n".join([line for line in collected if line.strip()]).strip()


def pipeline_status_from_logs(logs: str) -> str:
    if not logs:
        return "Not Run"
    if "Final Result: PASS" in logs or "Attempt 2: PASS" in logs:
        return "PASS"
    if "Final Result: FAIL" in logs or "Attempt 1: FAIL" in logs:
        return "FAIL"
    return "Unknown"


def render_status_badge(status: str):
    if status == "PASS":
        st.success("Pipeline Status: PASS")
    elif status == "FAIL":
        st.error("Pipeline Status: FAIL")
    else:
        st.info("Pipeline Status: Not Run")


def code_panel(title: str, path: Path, language: str = "python"):
    st.subheader(title)
    content = read_file(path)
    if content:
        st.code(content, language=language)
    else:
        st.caption("No data available.")


def text_panel(title: str, text: str):
    st.subheader(title)
    if text.strip():
        st.text(text)
    else:
        st.caption("No data available.")


def json_panel(title: str, data):
    st.subheader(title)
    if data is not None:
        st.json(data)
    else:
        st.caption("No data available.")


def render_pr_summary(pr_summary_text: str):
    st.subheader("📝 PR Summary")

    if not pr_summary_text.strip():
        st.caption("No PR summary available yet.")
        return

    lines = pr_summary_text.split("\n")

    title = ""
    summary_lines = []
    test_lines = []
    changed_files = []

    section = None

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("PR Title:"):
            title = line.replace("PR Title:", "").strip()
            section = None
            continue

        if line.startswith("Summary:"):
            section = "summary"
            continue

        if line.startswith("Tests:"):
            section = "tests"
            continue

        if line.startswith("Changed Files:"):
            section = "files"
            continue

        if line.startswith("-"):
            if section == "summary":
                summary_lines.append(line)
            elif section == "tests":
                test_lines.append(line)
            elif section == "files":
                changed_files.append(line)

    if title:
        st.markdown(f"## 🚀 {title}")
    else:
        st.markdown("## 🚀 Generated Pull Request Summary")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📌 Summary")
        if summary_lines:
            for item in summary_lines:
                st.markdown(item)
        else:
            st.caption("No summary points available.")

    with col2:
        st.markdown("### 🧪 Test Results")
        if test_lines:
            for item in test_lines:
                if "Passed: True" in item:
                    st.success(item)
                elif "Passed: False" in item:
                    st.error(item)
                else:
                    st.info(item)
        else:
            st.caption("No test result lines available.")

    st.markdown("### 📂 Changed Files")
    if changed_files:
        for item in changed_files:
            st.code(item.replace("- ", ""), language="bash")
    else:
        st.caption("No changed files listed.")


if "logs" not in st.session_state:
    st.session_state["logs"] = ""

if "last_stdout" not in st.session_state:
    st.session_state["last_stdout"] = ""

if "last_stderr" not in st.session_state:
    st.session_state["last_stderr"] = ""


st.title("🚀 AI DevOps Self-Healing Dashboard")
st.caption("Jira → Multi-Agent Analysis → Fix → Test → Result")

with st.sidebar:
    st.header("Controls")

    if st.button("🔄 Reset Demo Code", use_container_width=True):
        code, out, err = reset_demo()
        full_logs = out + ("\n" + err if err else "")
        st.session_state["logs"] = full_logs
        st.session_state["last_stdout"] = out
        st.session_state["last_stderr"] = err

        if code == 0:
            st.success("Demo code reset successfully.")
        else:
            st.error("Reset failed.")

    if st.button("▶️ Run Pipeline", use_container_width=True):
        with st.spinner("Running pipeline..."):
            code, out, err = run_pipeline()
            full_logs = out + ("\n" + err if err else "")
            st.session_state["logs"] = full_logs
            st.session_state["last_stdout"] = out
            st.session_state["last_stderr"] = err

            if "Final Result: PASS" in full_logs or "Attempt 2: PASS" in full_logs:
                st.success("Pipeline finished successfully.")
            elif "Final Result: FAIL" in full_logs:
                st.error("Pipeline finished but tests failed.")
            elif code == 0:
                st.success("Pipeline finished.")
            else:
                st.warning("Pipeline finished with errors.")

    st.divider()
    st.markdown("### How to use")
    st.markdown(
        """
1. Reset Demo Code  
2. Run Pipeline  
3. Review Jira, Analyzer, Code, PR Summary, and Results  
"""
    )

logs = st.session_state["logs"]
status = pipeline_status_from_logs(logs)
jira_text = extract_jira_block(logs)
analyzer_text = extract_analyzer_block(logs)
requirement_json = read_json(REQUIREMENT_FILE)
metrics_json = read_json(METRICS_FILE)
pr_summary_text = read_file(PR_SUMMARY_FILE)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Current Status", status)
with col2:
    st.metric("Jira Loaded", "Yes" if jira_text else "No")
with col3:
    st.metric("Analyzer Output", "Yes" if analyzer_text else "No")
with col4:
    st.metric("Fixed Code Saved", "Yes" if RAW_OUTPUT_FILE.exists() else "No")

render_status_badge(status)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "📌 Jira Ticket",
        "🧠 Analyzer",
        "💻 Code Comparison",
        "🤖 LLM Output",
        "📊 Metrics / Summary",
        "🖥️ Logs",
    ]
)

with tab1:
    text_panel("Fetched Jira Ticket", jira_text)

with tab2:
    left, right = st.columns([1, 1])

    with left:
        text_panel("Analyzer Output (Raw)", analyzer_text)

    with right:
        json_panel("Requirement / Structured Data", requirement_json)

with tab3:
    left, right = st.columns(2)

    with left:
        code_panel("Before Fix (`app_before_fix.py`)", BACKUP_FILE)

    with right:
        code_panel("Current Final Code (`app.py`)", APP_FILE)

with tab4:
    code_panel("Full LLM Output (`llm_last_output.py`)", RAW_OUTPUT_FILE)

with tab5:
    left, right = st.columns(2)

    with left:
        json_panel("Pipeline Metrics", metrics_json)

    with right:
        render_pr_summary(pr_summary_text)

with tab6:
    left, right = st.columns(2)

    with left:
        st.subheader("Pipeline Stdout")
        if st.session_state["last_stdout"]:
            st.code(st.session_state["last_stdout"], language="bash")
        else:
            st.caption("No stdout available.")

    with right:
        st.subheader("Pipeline Stderr")
        if st.session_state["last_stderr"]:
            st.code(st.session_state["last_stderr"], language="bash")
        else:
            st.caption("No stderr available.")