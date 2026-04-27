from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GitStatus:
    available: bool
    inside_repo: bool
    branch: str | None


def _run_git(args: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def get_git_status(cwd: str | None = None) -> GitStatus:
    if shutil.which("git") is None:
        return GitStatus(available=False, inside_repo=False, branch=None)

    inside = _run_git(["rev-parse", "--is-inside-work-tree"], cwd=cwd)
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        return GitStatus(available=True, inside_repo=False, branch=None)

    branch_result = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd)
    branch = branch_result.stdout.strip() if branch_result.returncode == 0 else None
    return GitStatus(available=True, inside_repo=True, branch=branch)


def write_demo_summary(path: str, content: str) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    return output


def write_text_file(path: str, content: str) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    return output


def read_text_file(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        return ""
    return file_path.read_text(encoding="utf-8")


def get_changed_files(cwd: str | None = None) -> list[str]:
    status = get_git_status(cwd=cwd)
    if not status.available or not status.inside_repo:
        return []

    result = _run_git(["diff", "--name-only"], cwd=cwd)
    if result.returncode != 0:
        return []

    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def get_diff_text(paths: list[str] | None = None, cwd: str | None = None) -> str:
    status = get_git_status(cwd=cwd)
    if not status.available or not status.inside_repo:
        return ""

    cmd = ["diff"]
    if paths:
        cmd.extend(paths)

    result = _run_git(cmd, cwd=cwd)
    if result.returncode != 0:
        return ""

    return result.stdout[:12000]


def safe_json_write(path: str, data: str) -> Path:
    return write_text_file(path, data)