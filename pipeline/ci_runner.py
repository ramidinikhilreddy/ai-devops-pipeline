from __future__ import annotations

import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class TestRunResult:
    returncode: int
    command: List[str]
    stdout: str
    stderr: str

    @property
    def passed(self) -> bool:
        return self.returncode == 0

    def to_dict(self) -> dict:
        return asdict(self)


def run_pytest(test_targets: Iterable[str] | None = None, cwd: str | None = None) -> TestRunResult:
    targets = list(test_targets or ["project/tests/test_app.py", "project/tests/test_risk.py"])
    command = [sys.executable, "-m", "pytest", *targets, "-v"]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    return TestRunResult(
        returncode=result.returncode,
        command=command,
        stdout=result.stdout,
        stderr=result.stderr,
    )
