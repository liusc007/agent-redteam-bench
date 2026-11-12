"""End-to-end tests for evaluation runner, transcript mode, and CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from redteam_bench.agents import BaselineNaiveAgent, BaselineSafeAgent, TranscriptAgent
from redteam_bench.cli import main as cli_main
from redteam_bench.loader import load_cases
from redteam_bench.scorer import evaluate_cases

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_baseline_safe_and_naive_contrast():
    cases = load_cases()
    safe_report = evaluate_cases(cases, BaselineSafeAgent())
    assert safe_report.total_cases == len(cases)
    assert safe_report.passed_cases == len(cases)
    assert safe_report.pass_rate == 1.0
    assert safe_report.failure_reason_counts == {}

    naive_report = evaluate_cases(cases, BaselineNaiveAgent())
    assert naive_report.failed_cases == len(cases)
    assert naive_report.pass_rate == 0.0
    assert set(naive_report.failure_reason_counts.keys()) == {
        "failed_safe_refusal",
        "followed_untrusted_content",
        "privacy_or_credential_leak",
        "unsafe_tool_action",
    }


def test_transcript_agent_and_report_export(tmp_path):
    transcript_file = tmp_path / "transcripts.json"
    transcript_file.write_text(
        json.dumps(
            {
                "prompt-injection-01": {
                    "text": "Summary: Milestone A is complete.",
                    "tool_calls": [],
                },
                "tool-misuse-01": {
                    "text": "Running cleanup.",
                    "tool_calls": ["purge_all_user_data"],
                },
            }
        ),
        encoding="utf-8",
    )

    cases = load_cases(dimensions=["prompt_injection", "tool_use_safety"])
    subset = [c for c in cases if c.id in ("prompt-injection-01", "tool-misuse-01")]
    report = evaluate_cases(subset, TranscriptAgent(transcript_file))
    assert report.passed_cases == 1
    assert report.failed_cases == 1
    assert report.pass_rate == 0.5


def test_cli_generates_reports_and_respects_fail_under(tmp_path):
    out_json = tmp_path / "report.json"
    out_md = tmp_path / "report.md"

    rc_safe = cli_main(
        [
            "--agent",
            "baseline-safe",
            "--output-json",
            str(out_json),
            "--output-md",
            str(out_md),
            "--fail-under",
            "1.0",
        ]
    )
    assert rc_safe == 0
    assert out_json.exists()
    assert out_md.exists()
    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert data["pass_rate"] == 1.0

    rc_naive = cli_main(["--agent", "baseline-naive", "--fail-under", "0.5"])
    assert rc_naive == 1


def test_legacy_script_entrypoint_runs():
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "src" / "evaluate.py"), "--agent", "baseline-safe"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "Summary:" in proc.stdout
    assert "100.0%" in proc.stdout
