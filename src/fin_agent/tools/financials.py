"""Annual income statements from the cache.

The part of this file worth slowing down on is what it does *not* do. JPM
reports no gross profit and no operating income — banks have no cost of goods
sold, so those fields are genuinely absent rather than zero, and the cache holds
`null` for every year. The rows pass through untouched:

- not `0`, because "reported as nothing" and "not reported" are different facts
  and only one of them is true
- not dropped, because a missing key hides the gap from everything downstream
- not derived, because nothing in the file lets you compute it

In week 7 the agent gets asked what JPM's gross margin was. The honest answer is
that it does not report one, and whether we get that answer is decided here.
"""

from __future__ import annotations

import json

from fin_agent import config

SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_income_statement",
        "description": "Annual income statement figures for one company, newest year first.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "enum": list(config.TICKERS),
                    "description": "One of the ten tickers this programme covers.",
                },
                "years": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "How many fiscal years to return, newest first.",
                },
            },
            "required": ["ticker"],
        },
    },
}


def get_income_statement(ticker: str, years: int = 3) -> list[dict]:
    """The last `years` annual income statements, newest fiscal year first."""
    path = config.cache_path(ticker, "income")
    if years < 1:
        raise ValueError(f"years must be at least 1, got {years}")

    rows = json.loads(path.read_text(encoding="utf-8"))["data"]
    rows = sorted(rows, key=lambda row: row["fiscal_year"], reverse=True)
    return rows[:years]
