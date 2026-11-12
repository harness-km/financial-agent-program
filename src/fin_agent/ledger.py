"""The cost ledger: one row per run, for the whole program.

An agent's cost is a design property rather than an accounting detail. By week 5
you read this file to tell whether compaction actually worked, which is why the
columns are fixed here in week 2 and never change afterwards.

Written with the `csv` module rather than an f-string, because a note containing
a comma is a matter of when, not whether.
"""

from __future__ import annotations

import csv
from datetime import UTC, datetime
from pathlib import Path

from fin_agent import config

LEDGER_HEADER = (
    "timestamp",
    "week",
    "model",
    "calls",
    "tokens_in",
    "tokens_out",
    "cost_usd",
    "note",
)


def log_run(
    *,
    week: str,
    model: str,
    calls: int,
    tokens_in: int,
    tokens_out: int,
    cost_usd: float,
    note: str = "",
    path: Path | None = None,
) -> Path:
    """Append one row to the cost ledger and return the file it was written to.

    Keyword-only on purpose: four integers in a row is exactly the signature an
    assistant fills in the wrong order, and a ledger that is quietly wrong is
    worse than no ledger at all.
    """
    path = path or config.LEDGER_PATH
    is_new = not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)

    row = {
        "timestamp": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "week": week,
        "model": model,
        "calls": calls,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": cost_usd,
        "note": note,
    }

    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_HEADER)
        if is_new:
            writer.writeheader()
        writer.writerow(row)

    return path
