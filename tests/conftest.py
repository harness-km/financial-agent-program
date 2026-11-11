"""Fixtures shared by every week's tests.

Tests are grouped by week in `tests/week_NN/`. A week's tests are the spec made
executable: if they pass, that week is done. Run just yours with
`pytest tests/week_03`.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="session")
def cache_dir() -> Path:
    """The cached market data folder."""
    path = ROOT / "cache"
    if not path.is_dir():
        pytest.skip("cache/ is missing — run scripts/doctor.py")
    return path


@pytest.fixture(scope="session")
def load_cached(cache_dir: Path):
    """Read one cached dataset: load_cached("AAPL", "income")."""

    def _load(ticker: str, dataset: str):
        path = cache_dir / ticker / f"{dataset}.json"
        if not path.is_file():
            pytest.skip(f"{path.relative_to(ROOT)} is missing")
        return json.loads(path.read_text(encoding="utf-8"))

    return _load


@pytest.fixture(scope="session")
def load_response():
    """Read one recorded model response: load_response("tool_call").

    These live in `tests/fixtures/model/` and exist so the code that parses a
    model's output can be tested without a key, a network call or a bill. See
    that folder's README for what each one is for.
    """

    def _load(name: str):
        path = FIXTURES / "model" / f"{name}.json"
        if not path.is_file():
            pytest.skip(f"{path.relative_to(ROOT)} is missing")
        return json.loads(path.read_text(encoding="utf-8"))

    return _load
