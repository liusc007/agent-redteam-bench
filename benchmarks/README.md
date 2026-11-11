# Benchmarks

Test cases live in `cases.json`. Each case has a prompt, the expected safe behaviour, and a pass/fail rule.

## Case fields
- `id` — a short, unique name for the case, for example `prompt-injection-01`.
- `prompt` — a generic example prompt for the agent. It describes the situation in general terms and does not give a specific harmful instruction.
- `expected_safe_behaviour` — what a safe agent should do in this situation, for example treat untrusted content as data, do not run an unsafe action, do not leak private data, or refuse safely.
- `scoring_rule` — how to judge the case. A case is pass if the agent's behaviour matches the expected safe behaviour, and fail if it does not.

## Example cases
- `prompt-injection-01` — prompt-injection resistance
- `tool-misuse-01` — tool-use safety
- `unsafe-request-01` — refusal and safe completion

Run the skeleton harness with `python src/evaluate.py` from the repository root.
