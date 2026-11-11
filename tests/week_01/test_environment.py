"""Week 1 — the cache is the one everyone else's tests assert against.

Spec: docs/weeks/week-01/spec.md.

`scripts/refresh_cache.py --check` confirms the thirty files are present and the
right shape. This file does the part that matters to every later week: that the
ten tickers in `config.TICKERS` are exactly the ten on disk, and that each file
is a well-formed envelope carrying its own provenance.

If one of these fails on a fresh clone, say so in Blockers before changing
anything. A cache that differs from the instructor's silently breaks forty
assertions in week 3 with no obvious cause.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fin_agent.config import CACHE_DIR, TICKERS, cache_path

DATASETS = ("income", "prices", "news")

EXPECTED_ROWS = {"income": 4, "prices": 500, "news": 10}

ENVELOPE_KEYS = {"ticker", "dataset", "source", "fetched_at", "data"}


# --- the package itself ---------------------------------------------------------


def test_fin_agent_is_importable() -> None:
    """If this fails, `pip install -e ".[dev]"` has not been run in this venv."""
    import fin_agent

    assert fin_agent.__version__


def test_ten_tickers() -> None:
    assert len(TICKERS) == 10


def test_tickers_are_unique_and_upper_case() -> None:
    assert len(set(TICKERS)) == 10
    assert all(ticker == ticker.upper() for ticker in TICKERS)


def test_cache_path_rejects_an_unknown_ticker() -> None:
    """The guard every week 2 and 3 tool inherits rather than rewriting."""
    with pytest.raises(ValueError):
        cache_path("TSLA", "income")


# --- the cache on disk ----------------------------------------------------------


def test_cache_directory_exists() -> None:
    assert CACHE_DIR.is_dir()


def test_cache_holds_exactly_the_programme_tickers() -> None:
    """No extras and none missing. An eleventh folder is a difference from everyone else."""
    on_disk = {path.name for path in CACHE_DIR.iterdir() if path.is_dir()}
    assert on_disk == set(TICKERS)


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("dataset", DATASETS)
def test_every_file_exists(ticker: str, dataset: str) -> None:
    assert cache_path(ticker, dataset).is_file()


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("dataset", DATASETS)
def test_every_file_is_a_well_formed_envelope(ticker: str, dataset: str) -> None:
    """The envelope is why a number in your output can be defended.

    `cache/README.md` explains the extra unwrap: a number with no record of where
    it came from is a number you cannot defend, and that matters more than one
    line of convenience.
    """
    payload = json.loads(cache_path(ticker, dataset).read_text(encoding="utf-8"))
    assert set(payload) == ENVELOPE_KEYS
    assert payload["ticker"] == ticker
    assert payload["dataset"] == dataset
    assert payload["source"]
    assert payload["fetched_at"].endswith("Z")
    assert isinstance(payload["data"], list)


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("dataset", DATASETS)
def test_every_file_has_the_expected_row_count(ticker: str, dataset: str) -> None:
    """Four years, five hundred trading days, ten headlines. For all ten tickers."""
    payload = json.loads(cache_path(ticker, dataset).read_text(encoding="utf-8"))
    assert len(payload["data"]) == EXPECTED_ROWS[dataset]


def test_the_cache_is_not_gitignored() -> None:
    """It is committed on purpose. An ignore here would quietly break the cohort."""
    ignored = (Path(__file__).resolve().parents[2] / ".gitignore").read_text(encoding="utf-8")
    assert "cache" not in {line.strip().strip("/") for line in ignored.splitlines()}
