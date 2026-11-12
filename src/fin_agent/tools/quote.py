"""The one tool week 2 offers the model: the latest close for one ticker.

There is no ticker check in this file. `config.cache_path` already raises
`ValueError` for anything outside `config.TICKERS`, so calling it gives us the
guard for free — and one check that everything reuses cannot disagree with
itself the way two checks eventually do.
"""

from __future__ import annotations

import json

from fin_agent import config


def get_latest_close(ticker: str) -> float:
    """The most recent closing price for one of the program's tickers."""
    path = config.cache_path(ticker, "prices")
    rows = json.loads(path.read_text(encoding="utf-8"))["data"]
    newest = max(rows, key=lambda row: row["date"])
    return float(newest["close"])
