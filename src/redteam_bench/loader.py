"""Benchmark case loader and schema validator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .models import VALID_DIMENSIONS, BenchmarkCase

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CASES_PATH = REPO_ROOT / "benchmarks" / "cases.json"

REQUIRED_FIELDS = (
    "id",
    "prompt",
    "expected_safe_behaviour",
    "scoring_rule",
)


def validate_case(raw: dict) -> None:
    """Validate required fields and basic types for one raw case dictionary."""
    if not isinstance(raw, dict):
        raise ValueError("Each benchmark case must be a JSON object.")
    for field_name in REQUIRED_FIELDS:
        value = raw.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Benchmark case missing non-empty string field: {field_name}")

    dimension = raw.get("dimension")
    if dimension is not None and dimension not in VALID_DIMENSIONS:
        raise ValueError(
            f"Case '{raw['id']}' has invalid dimension '{dimension}'. "
            f"Expected one of {VALID_DIMENSIONS}."
        )


def load_cases(
    cases_path: str | Path = DEFAULT_CASES_PATH,
    dimensions: Iterable[str] | None = None,
) -> list[BenchmarkCase]:
    """Load and validate benchmark cases from JSON."""
    path = Path(cases_path)
    with path.open(encoding="utf-8") as f:
        raw_items = json.load(f)

    if not isinstance(raw_items, list):
        raise ValueError(f"Expected a JSON list in {path}")

    seen_ids: set[str] = set()
    cases: list[BenchmarkCase] = []
    allowed_dims = set(dimensions) if dimensions else None

    for item in raw_items:
        validate_case(item)
        case_id = item["id"]
        if case_id in seen_ids:
            raise ValueError(f"Duplicate benchmark case id: {case_id}")
        seen_ids.add(case_id)

        case = BenchmarkCase.from_dict(item)
        if allowed_dims is not None and case.dimension not in allowed_dims:
            continue
        cases.append(case)

    return cases
