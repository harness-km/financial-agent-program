"""Daily OHLCV price history from the cache.

The cache is stored **oldest first** — 500 trading days from 2024-11-01 to
2026-10-30. So "the last thirty days" is the tail of the file, reversed, and a
tool that slices from the front returns November 2024 while sounding entirely
confident about it. That is the mistake this tool actually makes, which is why
`test_does_not_slice_from_the_front` exists.

Rows come back as they are cached: no rounding, no renaming, no derived columns.
Shaping what reaches the model is week 5's size cap, at the hook, once.
"""

from __future__ import annotations

import json

from fin_agent import config

SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_prices",
        "description": (
            "Daily open, high, low, close and volume for one company, newest trading day first."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "enum": list(config.TICKERS),
                    "description": "One of the ten tickers this programme covers.",
                },
                "days": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "How many of the most recent trading days to return.",
                },
            },
            "required": ["ticker"],
        },
    },
}


def get_prices(ticker: str, days: int = 30) -> list[dict]:
    """The last `days` trading days of OHLCV data, newest day first."""
    path = config.cache_path(ticker, "prices")
    if days < 1:
        raise ValueError(f"days must be at least 1, got {days}")

    rows = json.loads(path.read_text(encoding="utf-8"))["data"]
    rows = sorted(rows, key=lambda row: row["date"], reverse=True)
    return rows[:days]
