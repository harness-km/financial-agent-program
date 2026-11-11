"""Week 3 — the news tool.

Spec: docs/weeks/week-03/spec.md.

`get_news(ticker, limit=5)` reads `cache/<ticker>/news.json` and returns the most recent
`limit` items, newest first by `published`.

The cache is not sorted. For four of the ten tickers the first item in the file is not the
newest one, so `data[:limit]` returns the wrong headlines — and nothing downstream will
flag it, because the wrong headlines are still real headlines. MSFT is the clearest case
and has a test of its own below.
"""

from __future__ import annotations

import pytest

from fin_agent.config import TICKERS
from fin_agent.tools.news import get_news

FIELDS = {"title", "publisher", "url", "published"}
CACHED_ITEMS = 10


# --- shape ---------------------------------------------------------------------------


def test_returns_five_items_by_default() -> None:
    assert len(get_news("AAPL")) == 5


def test_exact_field_set() -> None:
    for item in get_news("AAPL"):
        assert set(item) == FIELDS


def test_items_are_the_cached_items_unchanged(load_cached) -> None:
    """No truncation, no summarising. Shaping the text is week 5's job, not this one."""
    cached = load_cached("MSFT", "news")["data"]
    newest = max(cached, key=lambda item: item["published"])
    assert get_news("MSFT", limit=1)[0] == newest


# --- sorting: the point of this tool -------------------------------------------------


@pytest.mark.parametrize("ticker", TICKERS)
def test_newest_first_for_every_ticker(ticker: str) -> None:
    published = [item["published"] for item in get_news(ticker, limit=CACHED_ITEMS)]
    assert published == sorted(published, reverse=True)


def test_msft_newest_item_is_not_the_first_in_the_file() -> None:
    """The file leads with 17:31:19; the newest is 18:56:20. Slicing returns the wrong one."""
    item = get_news("MSFT", limit=1)[0]
    assert item["published"] == "2026-11-10T18:56:20Z"
    assert item["publisher"] == "MT Newswires"
    assert item["title"] == (
        "Update: Market Chatter: Microsoft Urges Trump to Scrap Expected Ban on "
        "Chinese Data Center Tech"
    )


def test_msft_first_three_in_order() -> None:
    published = [item["published"] for item in get_news("MSFT", limit=3)]
    assert published == [
        "2026-11-10T18:56:20Z",
        "2026-11-10T18:50:00Z",
        "2026-11-10T18:22:45Z",
    ]


def test_msft_does_not_slice_from_the_front(load_cached) -> None:
    cached_titles = [item["title"] for item in load_cached("MSFT", "news")["data"][:3]]
    returned_titles = [item["title"] for item in get_news("MSFT", limit=3)]
    assert returned_titles != cached_titles


def test_aapl_newest_item() -> None:
    item = get_news("AAPL", limit=1)[0]
    assert item["published"] == "2026-11-10T19:00:00Z"
    assert item["title"] == "New iOS exploit could let apps steal crypto keys"


def test_jpm_oldest_item_sorts_last() -> None:
    """JPM's 03:14 item sits at index 8 in the file, ahead of an 11:04 item."""
    published = [item["published"] for item in get_news("JPM", limit=CACHED_ITEMS)]
    assert published[-1] == "2026-11-10T03:14:54Z"
    assert published[-2] == "2026-11-10T11:04:51Z"


def test_cat_spans_two_days() -> None:
    """Sorting on the time of day alone gets this ticker wrong."""
    published = [item["published"] for item in get_news("CAT", limit=CACHED_ITEMS)]
    assert published[0].startswith("2026-11-10")
    assert published[-1].startswith("2026-11-09")


# --- the limit argument --------------------------------------------------------------


def test_limit_one_returns_one() -> None:
    assert len(get_news("AAPL", limit=1)) == 1


def test_limit_beyond_the_cache_returns_what_exists() -> None:
    """Ten items are cached. Asking for fifty is not an error."""
    assert len(get_news("AAPL", limit=50)) == CACHED_ITEMS


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_ticker_has_ten_items(ticker: str) -> None:
    assert len(get_news(ticker, limit=CACHED_ITEMS)) == CACHED_ITEMS


@pytest.mark.parametrize("limit", [0, -1])
def test_rejects_non_positive_limit(limit: int) -> None:
    with pytest.raises(ValueError):
        get_news("AAPL", limit=limit)


# --- the security criterion ----------------------------------------------------------


@pytest.mark.parametrize("ticker", ["TSLA", "ORCL", "SPY"])
def test_rejects_ticker_outside_the_list(ticker: str) -> None:
    with pytest.raises(ValueError):
        get_news(ticker)


def test_rejects_lowercase_ticker() -> None:
    with pytest.raises(ValueError):
        get_news("aapl")


@pytest.mark.parametrize("ticker", ["", "AAPL/../JPM", "../../.env", "/etc/passwd"])
def test_rejects_malformed_ticker(ticker: str) -> None:
    with pytest.raises(ValueError):
        get_news(ticker)


# --- what the tool must not do ------------------------------------------------------


def test_returns_items_about_other_companies_too(load_cached) -> None:
    """AAPL's feed carries Nvidia and TSMC stories. The tool does not filter them out.

    This is deliberate. The tool reports what the source said; deciding what is
    relevant is the agent's job in week 4 and the model's problem in week 7, and a
    tool that silently drops rows is a tool whose output you cannot reconcile with
    its source.
    """
    titles = " ".join(item["title"] for item in get_news("AAPL", limit=CACHED_ITEMS))
    assert "Nvidia" in titles
