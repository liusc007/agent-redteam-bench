# src

This folder holds the evaluation harness for Agent Red-Team Bench.

## What is here
- `evaluate.py` — a simple evaluation skeleton. It reads `benchmarks/cases.json`, prints each case id and its expected safe behaviour, and outputs a pass / fail placeholder.

## Status
The harness is a skeleton only. It is not yet connected to a model. The TODO in `evaluate.py` marks where model integration and real scoring will be added.

## Run
From the repository root, run:

```
python src/evaluate.py
```
