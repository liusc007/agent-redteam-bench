# Agent Red-Team Bench

This repository is the research project for agent red-team evaluation described in my application.

## Research goal
Measure how AI agents behave under adversarial conditions, so we can make them safer. The benchmark tests whether an agent follows risky instructions, trusts misleading tool outputs, or completes unsafe requests, and records where it fails.

## Evaluation dimensions
- Prompt-injection resistance: do not follow instructions hidden in tool outputs or other untrusted content.
- Tool-use safety: do not run unsafe actions, and do not leak credentials or private data through tools.
- Refusal and safe completion: refuse or safely complete disallowed or risky requests.
- Privacy: do not leak private data.

## Method
Each test case has a prompt, the expected safe behaviour, and a scoring rule. Scoring is pass / fail per case, with reasons recorded. Summary metrics are the pass rate and a classification of failure reasons. See `docs/research-overview.md` for the background, threat model, method, and ethics.

## What this is not
This is defensive safety research only. It does not provide real attacks, exploits, or instructions to harm systems. All test cases are generic examples for evaluation in a controlled setting.

## Structure
- `benchmarks/` — test cases, including `cases.json` and `README.md`
- `docs/` — research overview
- `src/` — simple evaluation harness (to be added / in progress)
- `results/` — evaluation results (to be added)

## Status
Early work in progress. This version contains the full README, the research overview, the example cases, and the evaluation skeleton. The harness does not yet connect to a model.
