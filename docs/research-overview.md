# Research Overview

## Background

AI agents can read instructions, call tools, and act on behalf of a user. Those abilities are useful, but they also create new safety risks: an agent may follow a misleading instruction, run an unsafe action, or share private data. This project builds a small, controlled benchmark to measure those risks before agents are used in real settings.

## Threat model

This benchmark covers only generic evaluation categories. It does not describe real attacks, exploits, or harmful instructions.

- **Untrusted content**: instructions hidden in tool outputs, files, web pages, or other content the agent did not receive from the user.
- **Unsafe tool use**: a request or tool result that would lead the agent to run an unsafe action or share credentials or private data.
- **Risky or disallowed requests**: requests the agent should refuse or complete safely instead of complying.
- **Privacy leakage**: prompts or tool outputs that try to make the agent reveal private data or restricted tokens.

The test cases are deliberately generic and synthetic. The goal is to check the agent's decision, not to provide a working attack.

## Method

Each test case has a prompt, controlled untrusted context or mock tool surface, the expected safe behaviour, and a deterministic scoring rule. The evaluation harness in `src/evaluate.py` (`redteam_bench`) runs cases against either:

1. **Controlled synthetic baselines** (`baseline-safe` and `baseline-naive`) to validate pass/fail detection,
2. **Saved agent transcripts** (`transcript`) to score outputs from external agent frameworks offline, or
3. **An optional OpenAI-compatible model endpoint** (`openai-compatible`) using a user-supplied API key in environment variables.

## Scoring metrics

- **Pass rate**: the share of cases scored as pass.
- **Failure reason classification**: for each failed case, record the reason category (`followed_untrusted_content`, `unsafe_tool_action`, `privacy_or_credential_leak`, `failed_safe_refusal`).
- **Per-dimension results**: pass rates are reported separately for `prompt_injection`, `tool_use_safety`, `refusal_and_safe_completion`, and `privacy`.

## Ethics

This is defensive safety research only, for evaluation in a controlled setting. It does not provide real attacks, exploits, or instructions to harm systems. Test cases use generic synthetic placeholders and must not be used outside controlled evaluation.
