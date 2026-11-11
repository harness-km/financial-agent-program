"""Week 2 — the one tool the model is allowed to ask for.

Spec: docs/weeks/week-02/spec.md, part 1.

Before you write `src/fin_agent/tools/quote.py` this file fails at collection with
`ModuleNotFoundError: No module named 'fin_agent.tools.quote'`. That is the correct
first result, not a broken test.
"""

from __future__ import annotations

import pytest

from fin_agent.config import TICKERS
from fin_agent.tools.quote import get_latest_close

# The newest row in cache/<ticker>/prices.json is 2026-10-30 for every ticker.
LATEST_CLOSE = {
    "AAPL": 344.63,
    "MSFT": 521.91,
    "NVDA": 204.64,
    "GOOGL": 279.84,
    "AMZN": 240.35,
    "JPM": 337.04,
    "XOM": 187.25,
    "JNJ": 273.20,
    "WMT": 123.51,
    "CAT": 622.75,
}


def test_latest_close_aapl() -> None:
    assert get_latest_close("AAPL") == pytest.approx(344.63)


def test_latest_close_jpm() -> None:
    assert get_latest_close("JPM") == pytest.approx(337.04)


def test_latest_close_cat() -> None:
    assert get_latest_close("CAT") == pytest.approx(622.75)


def test_latest_close_is_a_float() -> None:
    """A number, not the row it came from and not a string."""
    result = get_latest_close("AAPL")
    assert isinstance(result, float)
    assert not isinstance(result, bool)


@pytest.mark.parametrize("ticker", TICKERS)
def test_latest_close_for_every_ticker(ticker: str) -> None:
    """All ten work, and all ten come from the newest row rather than the first one."""
    assert get_latest_close(ticker) == pytest.approx(LATEST_CLOSE[ticker])


def test_latest_close_takes_the_newest_row_not_the_first(load_cached) -> None:
    """The cache is oldest-first, so a naive `data[0]` returns the 2024 price."""
    rows = load_cached("AAPL", "prices")["data"]
    oldest = rows[0]["close"]
    assert get_latest_close("AAPL") != pytest.approx(oldest)


def test_latest_close_rejects_unknown_ticker() -> None:
    with pytest.raises(ValueError):
        get_latest_close("TSLA")


def test_latest_close_rejects_lowercase() -> None:
    """`config.TICKERS` is an exact list. Fail closed rather than guessing a case fix."""
    with pytest.raises(ValueError):
        get_latest_close("aapl")


def test_latest_close_rejects_empty_ticker() -> None:
    with pytest.raises(ValueError):
        get_latest_close("")


@pytest.mark.parametrize("ticker", ["AAPL/../JPM", "../cache/AAPL", "AAPL/prices"])
def test_latest_close_rejects_path_traversal(ticker: str) -> None:
    """The ticker is used to build a path, so the allowlist is the path control."""
    with pytest.raises(ValueError):
        get_latest_close(ticker)
