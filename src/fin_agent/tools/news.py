"""Recent headlines from the cache.

The file is not sorted. For four of the ten tickers the first item is not the
newest one — MSFT leads with 17:31 while its newest is 18:56 — so `data[:limit]`
returns the wrong headlines, and nothing downstream will notice, because the
wrong headlines are still real headlines.

Sorting is on the full `published` timestamp rather than the time of day: CAT's
oldest two items are from the previous date, and a tool that compared only
clock times would put them first.

The tool does not filter by relevance. AAPL's feed carries Nvidia and TSMC
stories and they come back. Deciding what is relevant is the agent's job from
week 4; a tool that silently drops rows is a tool whose output you cannot
reconcile against its source.
"""

from __future__ import annotations

import json

from fin_agent import config

SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_news",
        "description": "Recent news headlines for one company, newest first by publication time.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "enum": list(config.TICKERS),
                    "description": "One of the ten tickers this programme covers.",
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "How many of the most recent headlines to return.",
                },
            },
            "required": ["ticker"],
        },
    },
}


def get_news(ticker: str, limit: int = 5) -> list[dict]:
    """The `limit` most recent headlines, newest first by publication time."""
    path = config.cache_path(ticker, "news")
    if limit < 1:
        raise ValueError(f"limit must be at least 1, got {limit}")

    items = json.loads(path.read_text(encoding="utf-8"))["data"]
    items = sorted(items, key=lambda item: item["published"], reverse=True)
    return items[:limit]
