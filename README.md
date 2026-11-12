# Agent Red-Team Bench

[![CI](https://github.com/liusc007/agent-redteam-bench/actions/workflows/ci.yml/badge.svg)](https://github.com/liusc007/agent-redteam-bench/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

This repository is the research project for agent red-team evaluation described in my application.

## Research goal

Measure how AI agents behave under adversarial conditions, so we can make them safer. The benchmark tests whether an agent follows risky instructions, trusts misleading tool outputs, or completes unsafe requests, and records where it fails.

## Evaluation dimensions

- **Prompt-injection resistance (`prompt_injection`)**: do not follow instructions hidden in tool outputs or other untrusted content.
- **Tool-use safety (`tool_use_safety`)**: do not run unsafe actions, and do not leak credentials or private data through tools.
- **Refusal and safe completion (`refusal_and_safe_completion`)**: refuse or safely complete disallowed or risky requests.
- **Privacy (`privacy`)**: do not leak private data or synthetic secret tokens.

## Method

Each test case in `benchmarks/cases.json` defines a controlled scenario, the expected safe behaviour, deterministic scoring rules, and a failure category. Scoring is `pass` / `fail` per case, with explicit failure reasons recorded and aggregated into:

- **Overall pass rate**
- **Per-dimension pass rates** across all four safety dimensions
- **Failure reason classification** (`followed_untrusted_content`, `unsafe_tool_action`, `privacy_or_credential_leak`, `failed_safe_refusal`)

See `docs/research-overview.md` for the background, threat model, method, and ethics.

## What this is not

This is defensive safety research only. It does not provide real attacks, exploits, or instructions to harm systems. All test cases are generic synthetic examples for evaluation in a controlled setting.

## Quickstart

Zero external runtime dependencies are required for core evaluation (Python 3.10+ standard library).

```bash
# Run the reference safe-policy baseline (expected 100.0% pass rate)
python src/evaluate.py --agent baseline-safe \
  --output-json results/baseline_safe_report.json \
  --output-md results/baseline_safe_report.md

# Run the unguarded naive baseline to verify failure detection across all 4 dimensions
python src/evaluate.py --agent baseline-naive \
  --output-json results/baseline_naive_report.json \
  --output-md results/baseline_naive_report.md

# Score pre-recorded outputs from any external agent framework
python src/evaluate.py --agent transcript --transcripts path/to/transcripts.json

# Evaluate an OpenAI-compatible chat completions endpoint (requires OPENAI_API_KEY)
python src/evaluate.py --agent openai-compatible --model gpt-4o-mini --fail-under 0.9
```

You can also install the package locally and run the CLI directly:

```bash
pip install -e ".[dev]"
redteam-bench --agent baseline-safe
pytest -v
```

## Sample baseline comparison

Controlled synthetic baseline runs stored in `results/`:

| Baseline Agent | Passed / Total | Pass Rate | Purpose |
|---|---:|---:|---|
| `baseline-safe` | 12 / 12 | 100.0% | Verifies safe-behaviour scoring across all 4 dimensions |
| `baseline-naive` | 0 / 12 | 0.0% | Verifies deterministic detection of all 4 failure categories |

## Structure

- `benchmarks/` — controlled test cases (`cases.json`) and schema documentation (`README.md`)
- `docs/` — research overview, threat model, and ethics (`research-overview.md`)
- `src/` — modular evaluation harness (`redteam_bench` package + `evaluate.py` CLI)
- `results/` — reproducible JSON and Markdown evaluation reports
- `tests/` — automated unit and integration test suite
- `.github/workflows/` — continuous integration checks across Python 3.10–3.12

## Status

Working controlled evaluation harness. Includes 12 generic benchmark cases across all 4 evaluation dimensions, deterministic rule-based scoring, synthetic safe/naive baselines, offline transcript evaluation, an optional OpenAI-compatible model adapter, JSON/Markdown reporting, and automated pytest + GitHub Actions CI.
