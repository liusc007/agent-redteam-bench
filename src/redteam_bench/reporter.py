"""Report formatting and export utilities."""

from __future__ import annotations

import json
from pathlib import Path

from .models import EvaluationReport


def format_terminal_summary(report: EvaluationReport) -> str:
    """Format a concise human-readable summary for stdout."""
    lines = [
        f"Agent Red-Team Bench | Agent: {report.agent_name}",
        "=" * 60,
    ]
    for res in report.results:
        status = "PASS" if res.passed else f"FAIL ({res.failure_category})"
        lines.append(f"[{status}] {res.case_id} [{res.dimension}] - {res.reason}")

    lines.append("-" * 60)
    lines.append(
        f"Summary: {report.passed_cases}/{report.total_cases} passed "
        f"({report.pass_rate * 100:.1f}%)"
    )
    lines.append("Per-dimension pass rates:")
    for dim, stats in report.dimension_breakdown.items():
        lines.append(
            f"  - {dim}: {stats['passed']}/{stats['total']} "
            f"({stats['pass_rate'] * 100:.1f}%)"
        )
    if report.failure_reason_counts:
        lines.append("Failure reason classification:")
        for reason, count in report.failure_reason_counts.items():
            lines.append(f"  - {reason}: {count}")
    return "\n".join(lines)


def format_markdown_report(report: EvaluationReport) -> str:
    """Format a Markdown benchmark evaluation report."""
    lines = [
        f"# Evaluation Report: `{report.agent_name}`",
        "",
        f"- **Timestamp (UTC)**: `{report.timestamp_utc}`",
        f"- **Total Cases**: {report.total_cases}",
        f"- **Passed**: {report.passed_cases}",
        f"- **Failed**: {report.failed_cases}",
        f"- **Pass Rate**: **{report.pass_rate * 100:.1f}%**",
        "",
        "## Per-Dimension Results",
        "",
        "| Dimension | Passed | Failed | Total | Pass Rate |",
        "|---|---:|---:|---:|---:|",
    ]
    for dim, stats in report.dimension_breakdown.items():
        lines.append(
            f"| `{dim}` | {stats['passed']} | {stats['failed']} | "
            f"{stats['total']} | {stats['pass_rate'] * 100:.1f}% |"
        )

    lines.extend(["", "## Failure Reason Classification", ""])
    if report.failure_reason_counts:
        lines.append("| Failure Category | Count |")
        lines.append("|---|---:|")
        for category, count in report.failure_reason_counts.items():
            lines.append(f"| `{category}` | {count} |")
    else:
        lines.append("No failures recorded.")

    lines.extend(
        [
            "",
            "## Case-Level Results",
            "",
            "| Case ID | Dimension | Outcome | Failure Category | Reason |",
            "|---|---|---|---|---|",
        ]
    )
    for res in report.results:
        outcome = "PASS" if res.passed else "FAIL"
        cat = f"`{res.failure_category}`" if res.failure_category else "-"
        lines.append(
            f"| `{res.case_id}` | `{res.dimension}` | **{outcome}** | {cat} | {res.reason} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_reports(
    report: EvaluationReport,
    output_json: str | Path | None = None,
    output_md: str | Path | None = None,
) -> None:
    """Write JSON and/or Markdown reports to disk."""
    if output_json:
        json_path = Path(output_json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)

    if output_md:
        md_path = Path(output_md)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(format_markdown_report(report), encoding="utf-8")
