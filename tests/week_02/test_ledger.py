"""Week 2 — the cost ledger.

Spec: docs/weeks/week-02/spec.md, part 4.

Every test writes to a temporary file via the `path` argument, so running these never
touches your real `ledger.csv`. That the function takes `path` at all is why they can.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

import pytest

from fin_agent.ledger import LEDGER_HEADER, log_run

ROW = {
    "week": "02",
    "model": "gpt-5.4-mini",
    "calls": 1,
    "tokens_in": 312,
    "tokens_out": 24,
    "cost_usd": 0.000079,
    "note": "first raw tool call",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_ledger_header_is_the_agreed_columns() -> None:
    """Fixed, because week 5 reads this file to show compaction worked."""
    assert tuple(LEDGER_HEADER) == (
        "timestamp",
        "week",
        "model",
        "calls",
        "tokens_in",
        "tokens_out",
        "cost_usd",
        "note",
    )


def test_ledger_creates_file_with_header(tmp_path: Path) -> None:
    path = tmp_path / "ledger.csv"
    log_run(path=path, **ROW)

    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[0].split(",") == list(LEDGER_HEADER)
    assert len(lines) == 2


def test_ledger_returns_the_path_it_wrote(tmp_path: Path) -> None:
    path = tmp_path / "ledger.csv"
    assert log_run(path=path, **ROW) == path


def test_ledger_appends_without_repeating_header(tmp_path: Path) -> None:
    path = tmp_path / "ledger.csv"
    log_run(path=path, **ROW)
    log_run(path=path, **{**ROW, "note": "second run"})

    text = path.read_text(encoding="utf-8")
    assert text.count("tokens_in") == 1
    assert len(read_rows(path)) == 2


def test_ledger_row_round_trips(tmp_path: Path) -> None:
    path = tmp_path / "ledger.csv"
    log_run(path=path, **ROW)

    row = read_rows(path)[0]
    assert row["week"] == "02"
    assert row["model"] == "gpt-5.4-mini"
    assert int(row["calls"]) == 1
    assert int(row["tokens_in"]) == 312
    assert int(row["tokens_out"]) == 24
    assert float(row["cost_usd"]) == pytest.approx(0.000079)
    assert row["note"] == "first raw tool call"


def test_ledger_timestamp_is_iso8601(tmp_path: Path) -> None:
    path = tmp_path / "ledger.csv"
    log_run(path=path, **ROW)

    stamp = read_rows(path)[0]["timestamp"]
    parsed = datetime.fromisoformat(stamp)
    assert parsed.year >= 2026


def test_ledger_note_with_a_comma_survives(tmp_path: Path) -> None:
    """Use the csv module. Writing the line by hand with f-strings breaks here."""
    path = tmp_path / "ledger.csv"
    log_run(path=path, **{**ROW, "note": "uncapped run, on purpose"})

    assert read_rows(path)[0]["note"] == "uncapped run, on purpose"


def test_ledger_arguments_are_keyword_only(tmp_path: Path) -> None:
    """Four integers in a row is the signature an assistant fills in the wrong order."""
    with pytest.raises(TypeError):
        log_run("02", "gpt-5.4-mini", 1, 312, 24, 0.000079)  # type: ignore[misc]
