# src

This folder holds the evaluation harness for Agent Red-Team Bench.

## What is here

- `evaluate.py` — direct CLI wrapper (`python src/evaluate.py`) for convenience.
- `redteam_bench/` — modular evaluation package:
  - `models.py` — dataclasses for benchmark cases, captured agent responses, case results, and aggregated reports.
  - `loader.py` — loads and validates `benchmarks/cases.json` with optional dimension filtering.
  - `scorer.py` — deterministic rule-based scorer checking canary leakage, forbidden tool calls, injected directive markers, and required refusals.
  - `agents.py` — pluggable adapters (`BaselineSafeAgent`, `BaselineNaiveAgent`, `TranscriptAgent`, and `OpenAICompatibleAgent`).
  - `reporter.py` — terminal summary, JSON, and Markdown report generation.
  - `cli.py` — CLI argument parser and runner.

## Run

From the repository root:

```bash
python src/evaluate.py --agent baseline-safe
python src/evaluate.py --agent baseline-naive
python src/evaluate.py --agent transcript --transcripts path/to/transcripts.json
```
