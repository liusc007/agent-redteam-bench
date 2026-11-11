"""Simple evaluation skeleton for Agent Red-Team Bench.

Reads benchmarks/cases.json and prints each case.
No model is connected yet.
"""

import json
from pathlib import Path

CASES_PATH = Path(__file__).resolve().parent.parent / "benchmarks" / "cases.json"


def load_cases():
    with CASES_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def main():
    cases = load_cases()
    for case in cases:
        print(f"Case: {case['id']}")
        print(f"Expected safe behaviour: {case['expected_safe_behaviour']}")
        # TODO: connect to a model, run the agent on case["prompt"],
        # and score pass / fail using case["scoring_rule"].
        print("Result: TODO (pass/fail placeholder)")
        print()
    print(f"Total cases: {len(cases)}")
    print("Summary: TODO - pass rate and failure reasons not yet computed.")


if __name__ == "__main__":
    main()

















