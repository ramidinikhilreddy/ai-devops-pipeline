# project/risk.py

from dataclasses import dataclass


@dataclass
class RiskResult:
    score: float
    level: str


def assess_pipeline_risk(passed: bool, retries: int) -> RiskResult:
    """
    Simple risk calculation:
    - Passed quickly → LOW risk
    - Needed retries → MEDIUM
    - Failed → HIGH
    """

    if not passed:
        return RiskResult(score=1.0, level="HIGH")

    if retries == 0:
        return RiskResult(score=0.1, level="LOW")

    if retries == 1:
        return RiskResult(score=0.5, level="MEDIUM")

    return RiskResult(score=0.8, level="HIGH")