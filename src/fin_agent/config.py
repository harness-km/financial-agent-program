"""Settings every module reads, so no path or model name is typed twice.

Values come from the environment where they vary by person, and are hard-coded
where they must not vary — the ticker list especially. Those ten tickers are why
your results match everyone else's.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CACHE_DIR = ROOT / "cache"
LEDGER_PATH = ROOT / "ledger.csv"
SCRATCHPAD_DIR = ROOT / "scratchpad"

# Fixed for the whole program. Do not add to this list: the tests and the eval
# set assume exactly these, and matching results across the cohort is the point.
TICKERS: tuple[str, ...] = (
    "AAPL",
    "MSFT",
    "NVDA",
    "GOOGL",
    "AMZN",
    "JPM",
    "XOM",
    "JNJ",
    "WMT",
    "CAT",
)

# Keep this cheap. An architecture that works on a small model is a better
# architecture; a big model hides design problems rather than solving them.
MODEL = os.environ.get("FIN_AGENT_MODEL", "gpt-5.4-mini")

# Safety rails you build in week 4 and rely on for the rest of the program.
MAX_ITERATIONS = int(os.environ.get("FIN_AGENT_MAX_ITERATIONS", "10"))
REPEAT_CALL_LIMIT = int(os.environ.get("FIN_AGENT_REPEAT_CALL_LIMIT", "2"))


def cache_path(ticker: str, dataset: str) -> Path:
    """Path to one cached dataset, e.g. cache_path("AAPL", "income")."""
    if ticker not in TICKERS:
        raise ValueError(f"{ticker} is not one of the program's tickers: {TICKERS}")
    return CACHE_DIR / ticker / f"{dataset}.json"
