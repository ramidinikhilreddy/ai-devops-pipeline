from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict

from project.risk import assess_pipeline_risk as assess_pipeline_risk

class MetricsTracker:
    def __init__(self, output_path: str = "project/pipeline_metrics.json"):
        self.output_path = Path(output_path)
        self.started_at = time.time()

    def build_metrics(self, passed: bool, retries: int, with_rag: bool, extra: Dict[str, Any] | None = None) -> dict:
        duration_seconds = round(time.time() - self.started_at, 3)
        risk = assess_pipeline_risk(passed=passed, retries=retries)
        metrics = {
            "passed": passed,
            "retries": retries,
            "with_rag": with_rag,
            "duration_seconds": duration_seconds,
            "risk": {
                "score": risk.score,
                "level": risk.level,
            },
        }
        if extra:
            metrics.update(extra)
        return metrics

    def save(self, metrics: dict) -> Path:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        return self.output_path
