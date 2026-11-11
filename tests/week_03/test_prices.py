"""Week 3 — the price history tool.

Spec: docs/weeks/week-03/spec.md.

`get_prices(ticker, days=30)` reads `cache/<ticker>/prices.json` and returns the most
recent `days` rows, newest first.

The cache is stored oldest first — 2024-11-01 up to 2026-10-30, 500 trading days for
every ticker. So "the last thirty days" is the tail of the file reversed, and a tool that
slices from the front returns November 2024 while sounding entirely confident about it.
"""

from __future__ import annotations

import pytest

from fin_agent.config import TICKERS
from fin_agent.tools.prices import get_prices

FIELDS = {"date", "open", "high", "low", "close", "volume"}

NEWEST_DATE = "2026-10-30"
OLDEST_DATE = "2024-11-01"
CACHED_DAYS = 500


# --- shape ---------------------------------------------------------------------------


def test_returns_thirty_rows_by_default() -> None:
    assert len(get_prices("AAPL")) == 30


def test_newest_first() -> None:
    rows = get_prices("AAPL")
    dates = [row["date"] for row in rows]
    assert dates == sorted(dates, reverse=True)
    assert dates[0] == NEWEST_DATE


def test_exact_field_set() -> None:
    for row in get_prices("AAPL", days=5):
        assert set(row) == FIELDS


def test_rows_are_the_cached_rows_unchanged(load_cached) -> None:
    """No rounding, no renaming, no derived columns. Week 5 is where results get cut."""
    cached_newest = load_cached("AAPL", "prices")["data"][-1]
    assert get_prices("AAPL", days=1)[0] == cached_newest


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_ticker_covers_the_same_window(ticker: str) -> None:
    rows = get_prices(ticker, days=CACHED_DAYS)
    assert len(rows) == CACHED_DAYS
    assert rows[0]["date"] == NEWEST_DATE
    assert rows[-1]["date"] == OLDEST_DATE


# --- exact values --------------------------------------------------------------------


def test_aapl_newest_row() -> None:
    assert get_prices("AAPL", days=1)[0] == {
        "date": "2026-10-30",
        "open": 346.72,
        "high": 349.19,
        "low": 334.35,
        "close": 344.63,
        "volume": 67841600,
    }


def test_aapl_five_newest_closes() -> None:
    closes = [row["close"] for row in get_prices("AAPL", days=5)]
    assert closes == pytest.approx([344.63, 348.91, 343.83, 347.10, 343.91])


def test_aapl_five_newest_dates() -> None:
    dates = [row["date"] for row in get_prices("AAPL", days=5)]
    assert dates == [
        "2026-10-30",
        "2026-10-29",
        "2026-10-28",
        "2026-10-27",
        "2026-10-26",
    ]


def test_thirtieth_row_back() -> None:
    """Thirty trading days back from 2026-10-30 is 2026-09-21, not 2026-09-30."""
    rows = get_prices("AAPL", days=30)
    assert rows[-1]["date"] == "2026-09-21"
    assert rows[-1]["close"] == pytest.approx(338.98)


def test_jpm_newest_close() -> None:
    assert get_prices("JPM", days=1)[0]["close"] == pytest.approx(337.04)


def test_cat_newest_row() -> None:
    row = get_prices("CAT", days=1)[0]
    assert row["close"] == pytest.approx(622.75)
    assert row["volume"] == 5300400


def test_volume_stays_an_integer() -> None:
    assert isinstance(get_prices("AAPL", days=1)[0]["volume"], int)


# --- the days argument ---------------------------------------------------------------


def test_days_one_returns_one() -> None:
    assert len(get_prices("AAPL", days=1)) == 1


def test_days_beyond_the_cache_returns_what_exists() -> None:
    """500 days are cached. Asking for 5,000 is not an error."""
    rows = get_prices("AAPL", days=5000)
    assert len(rows) == CACHED_DAYS
    assert rows[-1]["date"] == OLDEST_DATE


@pytest.mark.parametrize("days", [0, -1, -30])
def test_rejects_non_positive_days(days: int) -> None:
    with pytest.raises(ValueError):
        get_prices("AAPL", days=days)


def test_does_not_slice_from_the_front(load_cached) -> None:
    """The failure this tool is most likely to have, named and asserted against."""
    oldest_thirty = [row["date"] for row in load_cached("AAPL", "prices")["data"][:30]]
    returned = [row["date"] for row in get_prices("AAPL", days=30)]
    assert returned != oldest_thirty
    assert returned != list(reversed(oldest_thirty))


# --- the security criterion ----------------------------------------------------------


@pytest.mark.parametrize("ticker", ["TSLA", "ORCL", "SPY"])
def test_rejects_ticker_outside_the_list(ticker: str) -> None:
    with pytest.raises(ValueError):
        get_prices(ticker)


def test_rejects_lowercase_ticker() -> None:
    with pytest.raises(ValueError):
        get_prices("aapl")


@pytest.mark.parametrize("ticker", ["", "AAPL/../JPM", "../../.env", "/etc/passwd"])
def test_rejects_malformed_ticker(ticker: str) -> None:
    with pytest.raises(ValueError):
        get_prices(ticker)
