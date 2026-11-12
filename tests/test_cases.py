"""Tests for benchmark case loading and schema validation."""

from __future__ import annotations

import json

import pytest

from redteam_bench.loader import DEFAULT_CASES_PATH, load_cases, validate_case
from redteam_bench.models import VALID_DIMENSIONS


def test_default_cases_cover_all_dimensions():
    cases = load_cases(DEFAULT_CASES_PATH)
    assert len(cases) >= 12
    ids = {c.id for c in cases}
    assert {"prompt-injection-01", "tool-misuse-01", "unsafe-request-01"}.issubset(ids)
    dimensions = {c.dimension for c in cases}
    assert dimensions == set(VALID_DIMENSIONS)


def test_dimension_filter():
    privacy_cases = load_cases(DEFAULT_CASES_PATH, dimensions=["privacy"])
    assert len(privacy_cases) >= 3
    assert all(c.dimension == "privacy" for c in privacy_cases)


def test_duplicate_id_rejected(tmp_path):
    bad_file = tmp_path / "dup.json"
    bad_file.write_text(
        json.dumps(
            [
                {
                    "id": "dup-01",
                    "dimension": "privacy",
                    "prompt": "p1",
                    "expected_safe_behaviour": "e1",
                    "scoring_rule": "s1",
                },
                {
                    "id": "dup-01",
                    "dimension": "privacy",
                    "prompt": "p2",
                    "expected_safe_behaviour": "e2",
                    "scoring_rule": "s2",
                },
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Duplicate"):
        load_cases(bad_file)


def test_invalid_dimension_rejected():
    with pytest.raises(ValueError, match="invalid dimension"):
        validate_case(
            {
                "id": "bad-dim-01",
                "dimension": "unknown_dim",
                "prompt": "p",
                "expected_safe_behaviour": "e",
                "scoring_rule": "s",
            }
        )
