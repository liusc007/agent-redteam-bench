# Benchmarks

Test cases live in `cases.json`. Each case describes a controlled defensive scenario, the expected safe behaviour, and a deterministic pass/fail rule.

## Case fields

- `id` — a short, unique name for the case, for example `prompt-injection-01`.
- `dimension` — one of `prompt_injection`, `tool_use_safety`, `refusal_and_safe_completion`, or `privacy`.
- `prompt` — a generic description of the evaluation scenario.
- `user_turn` — the benign or adversarial user-facing prompt passed to the agent adapter.
- `untrusted_context` — optional synthetic tool output or retrieved snippet containing untrusted content or canary placeholders.
- `available_tools` — mock tool names exposed to the agent during evaluation.
- `forbidden_actions` — mock unsafe tool names that must not be invoked.
- `forbidden_markers` — synthetic override strings that must not be echoed or followed.
- `canary_tokens` — synthetic placeholder tokens that must never be leaked.
- `require_refusal` — whether an explicit refusal or safety boundary explanation is required.
- `expected_safe_behaviour` — what a safe agent should do in this situation.
- `scoring_rule` — human-readable pass/fail rule for the case.
- `failure_category` — classification recorded on failure (`followed_untrusted_content`, `unsafe_tool_action`, `privacy_or_credential_leak`, `failed_safe_refusal`).

## Current suite (12 controlled cases)

- `prompt-injection-01` .. `03` — prompt-injection resistance
- `tool-misuse-01` .. `03` — tool-use safety
- `unsafe-request-01` .. `03` — refusal and safe completion
- `privacy-01` .. `03` — privacy and synthetic secret protection

Run the harness from the repository root:

```bash
python src/evaluate.py --agent baseline-safe
```
