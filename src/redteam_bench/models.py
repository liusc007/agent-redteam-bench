"""Data models for Agent Red-Team Bench."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

VALID_DIMENSIONS = (
    "prompt_injection",
    "tool_use_safety",
    "refusal_and_safe_completion",
    "privacy",
)

VALID_FAILURE_CATEGORIES = (
    "followed_untrusted_content",
    "unsafe_tool_action",
    "privacy_or_credential_leak",
    "failed_safe_refusal",
    "policy_violation",
)


@dataclass(frozen=True)
class BenchmarkCase:
    """Single controlled evaluation case."""

    id: str
    dimension: str
    prompt: str
    expected_safe_behaviour: str
    scoring_rule: str
    user_turn: str = ""
    untrusted_context: str = ""
    available_tools: tuple[str, ...] = ()
    forbidden_actions: tuple[str, ...] = ()
    forbidden_markers: tuple[str, ...] = ()
    canary_tokens: tuple[str, ...] = ()
    require_refusal: bool = False
    failure_category: str = "policy_violation"

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "BenchmarkCase":
        return cls(
            id=str(raw["id"]),
            dimension=str(raw.get("dimension", "prompt_injection")),
            prompt=str(raw["prompt"]),
            expected_safe_behaviour=str(raw["expected_safe_behaviour"]),
            scoring_rule=str(raw["scoring_rule"]),
            user_turn=str(raw.get("user_turn") or raw["prompt"]),
            untrusted_context=str(raw.get("untrusted_context", "")),
            available_tools=tuple(str(t) for t in raw.get("available_tools", [])),
            forbidden_actions=tuple(str(a) for a in raw.get("forbidden_actions", [])),
            forbidden_markers=tuple(str(m) for m in raw.get("forbidden_markers", [])),
            canary_tokens=tuple(str(c) for c in raw.get("canary_tokens", [])),
            require_refusal=bool(raw.get("require_refusal", False)),
            failure_category=str(raw.get("failure_category", "policy_violation")),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AgentResponse:
    """Captured agent output for one benchmark case."""

    text: str
    tool_calls: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CaseResult:
    """Deterministic pass/fail outcome for a single benchmark case."""

    case_id: str
    dimension: str
    passed: bool
    reason: str
    failure_category: str | None
    agent_text: str
    tool_calls: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvaluationReport:
    """Aggregated benchmark run report."""

    agent_name: str
    timestamp_utc: str
    total_cases: int
    passed_cases: int
    failed_cases: int
    pass_rate: float
    dimension_breakdown: dict[str, dict[str, Any]]
    failure_reason_counts: dict[str, int]
    results: tuple[CaseResult, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["results"] = [r.to_dict() for r in self.results]
        return payload
