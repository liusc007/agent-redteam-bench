"""Command-line wrapper for Agent Red-Team Bench.

Allows running directly from repository root:
    python src/evaluate.py
"""

from __future__ import annotations

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from redteam_bench.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
