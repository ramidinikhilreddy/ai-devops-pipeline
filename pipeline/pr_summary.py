from llm.agents import run_pr_summary_agent
from pipeline.git_utils import get_changed_files, get_diff_text, write_text_file


def generate_pr_summary(
    llm,
    jira_ticket: str,
    pytest_output: str,
    test_passed: bool,
    retries_used: int,
    output_path: str = "project/pr_summary.txt",
) -> str:

    changed_files = get_changed_files()

    candidate_paths = changed_files if changed_files else [
        "project",
        "pipeline",
        "llm",
        "jira",
        "scripts",
    ]

    diff_text = get_diff_text(candidate_paths)

    summary_text = run_pr_summary_agent(
        llm=llm,
        jira_ticket=jira_ticket,
        changed_files=changed_files,
        diff_text=diff_text,
        pytest_output=pytest_output,
        test_passed=test_passed,
        retries_used=retries_used,
    )

    if summary_text.strip():
        write_text_file(output_path, summary_text)

    return summary_text