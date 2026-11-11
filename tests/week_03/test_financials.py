"""Week 3 — the income statement tool.

Spec: docs/weeks/week-03/spec.md.

`get_income_statement(ticker, years=3)` reads `cache/<ticker>/income.json`, returns the
rows newest first, and raises `ValueError` for any ticker outside `config.TICKERS`.

The JPM tests are the ones to read first. Banks do not report gross profit or operating
income, so those fields are `None` in the cache for every year. A tool that turns them
into `0`, drops the key, or works a number out from revenue has invented data — and the
agent you build in week 4 has no way to know it happened.
"""

from __future__ import annotations

import pytest

from fin_agent.config import TICKERS
from fin_agent.tools.financials import get_income_statement

FIELDS = {"fiscal_year", "revenue", "gross_profit", "operating_income", "net_income"}

# The newest fiscal year in the cache, per ticker. Four of the ten have closed FY2026
# already; the rest are still on FY2025. Code that hard-codes "last year" is wrong for
# one group or the other.
LATEST_FY = {
    "AAPL": 2026,
    "MSFT": 2026,
    "NVDA": 2026,
    "WMT": 2026,
    "GOOGL": 2025,
    "AMZN": 2025,
    "JPM": 2025,
    "XOM": 2025,
    "JNJ": 2025,
    "CAT": 2025,
}


# --- shape ---------------------------------------------------------------------------


def test_returns_three_years_by_default() -> None:
    rows = get_income_statement("AAPL")
    assert len(rows) == 3


def test_newest_first() -> None:
    rows = get_income_statement("AAPL")
    assert [row["fiscal_year"] for row in rows] == [2026, 2025, 2024]


def test_googl_is_a_year_behind_aapl() -> None:
    """Not every ticker's latest year is the same. The tool must not assume one."""
    rows = get_income_statement("GOOGL")
    assert [row["fiscal_year"] for row in rows] == [2025, 2024, 2023]


def test_exact_field_set() -> None:
    """The five agreed keys and nothing else — no `ticker`, no `source`, no extras."""
    for row in get_income_statement("AAPL"):
        assert set(row) == FIELDS


def test_reads_the_data_key_not_the_envelope() -> None:
    """`payload["data"]`, not `payload`. The provenance fields stay out of the rows."""
    row = get_income_statement("AAPL")[0]
    assert "dataset" not in row
    assert "fetched_at" not in row


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_ticker_has_at_least_three_years(ticker: str) -> None:
    rows = get_income_statement(ticker, years=3)
    assert len(rows) == 3
    years = [row["fiscal_year"] for row in rows]
    assert years == sorted(years, reverse=True)
    assert years[0] == LATEST_FY[ticker]


# --- exact values --------------------------------------------------------------------


def test_aapl_latest_year_values() -> None:
    row = get_income_statement("AAPL")[0]
    assert row == {
        "fiscal_year": 2026,
        "revenue": 478834000000,
        "gross_profit": 233602000000,
        "operating_income": 158063000000,
        "net_income": 132175000000,
    }


def test_msft_latest_revenue() -> None:
    assert get_income_statement("MSFT")[0]["revenue"] == 331839000000


def test_nvda_oldest_of_three() -> None:
    rows = get_income_statement("NVDA", years=3)
    assert rows[-1] == {
        "fiscal_year": 2024,
        "revenue": 60922000000,
        "gross_profit": 44301000000,
        "operating_income": 32972000000,
        "net_income": 29760000000,
    }


def test_amzn_negative_net_income_is_preserved() -> None:
    """FY2022 was a loss. A tool that clamps at zero is lying about a real year."""
    rows = get_income_statement("AMZN", years=4)
    assert rows[-1]["fiscal_year"] == 2022
    assert rows[-1]["net_income"] == -2722000000


# --- JPM: the fields a bank does not report ------------------------------------------


def test_jpm_missing_fields_stay_none() -> None:
    row = get_income_statement("JPM")[0]
    assert row["gross_profit"] is None
    assert row["operating_income"] is None


def test_jpm_missing_fields_are_not_zero() -> None:
    """`None` means "not reported". `0` means "reported as nothing". They differ."""
    row = get_income_statement("JPM")[0]
    assert row["gross_profit"] != 0
    assert row["operating_income"] != 0


def test_jpm_keys_are_present_even_when_empty() -> None:
    """Dropping the key hides the gap. Downstream code should see it, not miss it."""
    for row in get_income_statement("JPM", years=4):
        assert set(row) == FIELDS


def test_jpm_reported_fields_are_intact() -> None:
    row = get_income_statement("JPM")[0]
    assert row["fiscal_year"] == 2025
    assert row["revenue"] == 181847000000
    assert row["net_income"] == 57048000000


def test_jpm_gross_profit_is_never_derived() -> None:
    """All four years. None of them acquires a number from somewhere."""
    rows = get_income_statement("JPM", years=4)
    assert [row["gross_profit"] for row in rows] == [None, None, None, None]


# --- the years argument --------------------------------------------------------------


def test_years_one_returns_only_the_latest() -> None:
    rows = get_income_statement("AAPL", years=1)
    assert len(rows) == 1
    assert rows[0]["fiscal_year"] == 2026


def test_years_four_returns_four() -> None:
    rows = get_income_statement("AAPL", years=4)
    assert [row["fiscal_year"] for row in rows] == [2026, 2025, 2024, 2023]


def test_years_beyond_the_cache_returns_what_exists() -> None:
    """Four years are cached. Asking for ten is not an error; inventing six is."""
    assert len(get_income_statement("AAPL", years=10)) == 4


@pytest.mark.parametrize("years", [0, -1])
def test_rejects_non_positive_years(years: int) -> None:
    with pytest.raises(ValueError):
        get_income_statement("AAPL", years=years)


# --- the security criterion ----------------------------------------------------------


@pytest.mark.parametrize("ticker", ["TSLA", "ORCL", "BRK.B", "SPY"])
def test_rejects_ticker_outside_the_list(ticker: str) -> None:
    with pytest.raises(ValueError):
        get_income_statement(ticker)


def test_rejects_lowercase_ticker() -> None:
    """The allowlist is exact. Quietly upper-casing it is a guess, not a validation."""
    with pytest.raises(ValueError):
        get_income_statement("aapl")


@pytest.mark.parametrize("ticker", ["", " ", "AAPL ", "AAPL,JPM"])
def test_rejects_malformed_ticker(ticker: str) -> None:
    with pytest.raises(ValueError):
        get_income_statement(ticker)


@pytest.mark.parametrize(
    "ticker",
    ["AAPL/../JPM", "../../.env", "AAPL/income", "/etc/passwd", "..\\..\\.env"],
)
def test_rejects_path_traversal(ticker: str) -> None:
    """The ticker becomes part of a file path. The allowlist is what makes that safe."""
    with pytest.raises(ValueError):
        get_income_statement(ticker)


def test_error_message_names_the_ticker() -> None:
    """A refusal the learner can debug, and that the model cannot mistake for data."""
    with pytest.raises(ValueError, match="TSLA"):
        get_income_statement("TSLA")
