"""Controlled defensive evaluation harness for Agent Red-Team Bench."""

from .agents import (
    AgentAdapter,
    BaselineNaiveAgent,
    BaselineSafeAgent,
    OpenAICompatibleAgent,
    TranscriptAgent,
)
from .loader import DEFAULT_CASES_PATH, load_cases, validate_case
from .models import AgentResponse, BenchmarkCase, CaseResult, EvaluationReport
from .reporter import format_markdown_report, format_terminal_summary, write_reports
from .scorer import evaluate_cases, score_case

__all__ = [
    "AgentAdapter",
    "AgentResponse",
    "BaselineNaiveAgent",
    "BaselineSafeAgent",
    "BenchmarkCase",
    "CaseResult",
    "DEFAULT_CASES_PATH",
    "EvaluationReport",
    "OpenAICompatibleAgent",
    "TranscriptAgent",
    "evaluate_cases",
    "format_markdown_report",
    "format_terminal_summary",
    "load_cases",
    "score_case",
    "validate_case",
    "write_reports",
]
