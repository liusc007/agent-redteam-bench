"""CLI entrypoint for Agent Red-Team Bench."""

from __future__ import annotations

import argparse
from typing import Sequence

from .agents import (
    AgentAdapter,
    BaselineNaiveAgent,
    BaselineSafeAgent,
    OpenAICompatibleAgent,
    TranscriptAgent,
)
from .loader import DEFAULT_CASES_PATH, load_cases
from .models import VALID_DIMENSIONS
from .reporter import format_terminal_summary, write_reports
from .scorer import evaluate_cases


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="redteam-bench",
        description="Controlled defensive evaluation harness for Agent Red-Team Bench.",
    )
    parser.add_argument(
        "--agent",
        choices=("baseline-safe", "baseline-naive", "transcript", "openai-compatible"),
        default="baseline-safe",
        help="Agent adapter to evaluate (default: baseline-safe).",
    )
    parser.add_argument(
        "--cases",
        default=str(DEFAULT_CASES_PATH),
        help="Path to benchmark cases JSON (default: benchmarks/cases.json).",
    )
    parser.add_argument(
        "--dimension",
        choices=VALID_DIMENSIONS,
        action="append",
        help="Filter evaluation to one or more specific dimensions.",
    )
    parser.add_argument(
        "--transcripts",
        help="Path to pre-recorded responses JSON when --agent transcript is selected.",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="Model name for --agent openai-compatible (default: gpt-4o-mini).",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Custom OpenAI-compatible base URL (or set OPENAI_BASE_URL).",
    )
    parser.add_argument(
        "--output-json",
        help="Optional path to save the full structured JSON report.",
    )
    parser.add_argument(
        "--output-md",
        help="Optional path to save the Markdown summary report.",
    )
    parser.add_argument(
        "--fail-under",
        type=float,
        default=None,
        help="Exit with code 1 if overall pass rate is below this threshold (0.0 - 1.0).",
    )
    return parser


def _resolve_agent(args: argparse.Namespace) -> AgentAdapter:
    if args.agent == "baseline-safe":
        return BaselineSafeAgent()
    if args.agent == "baseline-naive":
        return BaselineNaiveAgent()
    if args.agent == "transcript":
        if not args.transcripts:
            raise ValueError("--transcripts <path> is required when --agent transcript is used.")
        return TranscriptAgent(args.transcripts)
    if args.agent == "openai-compatible":
        return OpenAICompatibleAgent(model=args.model, base_url=args.base_url)
    raise ValueError(f"Unsupported agent type: {args.agent}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    cases = load_cases(args.cases, dimensions=args.dimension)
    agent = _resolve_agent(args)
    report = evaluate_cases(cases, agent)

    print(format_terminal_summary(report))
    write_reports(report, output_json=args.output_json, output_md=args.output_md)

    if args.fail_under is not None and report.pass_rate < args.fail_under:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
