# Research Overview

## Background
AI agents can read instructions, call tools, and act on behalf of a user. Those abilities are useful, but they also create new safety risks: an agent may follow a misleading instruction, run an unsafe action, or share private data. This project builds a small, controlled benchmark to measure those risks before agents are used in real settings.

## Threat model
This benchmark covers only generic evaluation categories. It does not describe real attacks, exploits, or harmful instructions.

- Untrusted content: instructions hidden in tool outputs, files, web pages, or other content the agent did not receive from the user.
- Unsafe tool use: a request or tool result that would lead the agent to run an unsafe action or share credentials or private data.
- Risky or disallowed requests: requests the agent should refuse or complete safely instead of complying.
- Privacy leakage: prompts or tool outputs that try to make the agent reveal private data.

The test cases are deliberately generic. The goal is to check the agent's decision, not to provide a working attack.

## Method
Each test case has a prompt, the expected safe behaviour, and a scoring rule. The evaluation harness in `src/evaluate.py` lists the cases and records a pass / fail result for each one, with a reason. No real model is connected yet; the harness is a skeleton with a TODO for model integration.

## Scoring metrics
- Pass rate: the share of cases scored as pass.
- Failure reason classification: for each failed case, record the reason, for example following untrusted content, running an unsafe action, leaking private data, or failing to refuse safely.
- Per-dimension results: pass rates can be reported separately for prompt-injection resistance, tool-use safety, refusal and safe completion, and privacy.

## Ethics
This is defensive safety research only, for evaluation in a controlled setting. It does not provide real attacks, exploits, or instructions to harm systems. Test cases use generic examples and must not be used outside controlled evaluation.
