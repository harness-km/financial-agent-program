#!/usr/bin/env python3
"""Fetch the programme's market data into cache/ so every run is deterministic.

The cache is committed to the repository on purpose: the tests assert exact
values against it, so your results match everyone else's. That also means
re-running this is an instructor action, not a casual one — new numbers break
the tests that asserted the old ones.

Usage:
    python scripts/refresh_cache.py --only AAPL     # smoke test one ticker
    python scripts/refresh_cache.py                 # all ten
    python scripts/refresh_cache.py --check         # validate what is there

Each file is an envelope, so the data carries its own provenance:

    {
      "ticker": "AAPL",
      "dataset": "income",
      "source": "yfinance",
      "fetched_at": "2026-11-11T00:30:00Z",
      "data": [ ... ]
    }

Requires yfinance, which arrives with `pip install -e ".[dev]"`.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from fin_agent.config import CACHE_DIR, TICKERS  # noqa: E402

DATASETS = ("income", "prices", "news")

# Pinned rather than relative ("2y"), so a re-fetch reproduces the same rows.
# Moving these is an instructor change that invalidates every price assertion.
PRICE_START = "2024-11-01"
PRICE_END = "2026-11-01"

# yfinance row labels drift between versions, so each field lists the labels
# seen in the wild, tried in order.
INCOME_FIELDS: dict[str, tuple[str, ...]] = {
    "revenue": ("Total Revenue", "TotalRevenue", "Revenue"),
    "gross_profit": ("Gross Profit", "GrossProfit"),
    "operating_income": ("Operating Income", "OperatingIncome"),
    "net_income": ("Net Income", "NetIncome", "Net Income Common Stockholders"),
}


def now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def envelope(ticker: str, dataset: str, data: list) -> dict:
    return {
        "ticker": ticker,
        "dataset": dataset,
        "source": "yfinance",
        "fetched_at": now_iso(),
        "data": data,
    }


def write(ticker: str, dataset: str, data: list) -> Path:
    path = CACHE_DIR / ticker / f"{dataset}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(envelope(ticker, dataset, data), indent=2) + "\n", encoding="utf-8")
    return path


def pick_row(frame, labels: tuple[str, ...]):
    """First matching row label, or None. yfinance renames these between versions."""
    for label in labels:
        if label in frame.index:
            return frame.loc[label]
    return None


def fetch_income(tk, ticker: str) -> list[dict]:
    frame = tk.income_stmt
    if frame is None or frame.empty:
        raise RuntimeError("income_stmt came back empty")

    rows: list[dict] = []
    for column in frame.columns:
        row: dict = {"fiscal_year": int(getattr(column, "year", 0)) or str(column)}
        for field, labels in INCOME_FIELDS.items():
            series = pick_row(frame, labels)
            value = None if series is None else series.get(column)
            try:
                row[field] = None if value is None or value != value else int(value)
            except (TypeError, ValueError):
                row[field] = None
        rows.append(row)

    # yfinance returns a trailing column with no figures in it. Drop any row
    # where every metric is missing rather than cache a row of nulls.
    metrics = tuple(INCOME_FIELDS)
    rows = [r for r in rows if any(r[m] is not None for m in metrics)]
    if not rows:
        raise RuntimeError("every income row came back empty")

    rows.sort(key=lambda r: r["fiscal_year"], reverse=True)
    return rows


def fetch_prices(tk, ticker: str) -> list[dict]:
    frame = tk.history(start=PRICE_START, end=PRICE_END, interval="1d", auto_adjust=False)
    if frame is None or frame.empty:
        raise RuntimeError(f"no price history for {PRICE_START}..{PRICE_END}")

    rows = []
    for stamp, row in frame.iterrows():
        rows.append(
            {
                "date": stamp.strftime("%Y-%m-%d"),
                "open": round(float(row["Open"]), 4),
                "high": round(float(row["High"]), 4),
                "low": round(float(row["Low"]), 4),
                "close": round(float(row["Close"]), 4),
                "volume": int(row["Volume"]),
            }
        )
    return rows


def fetch_news(tk, ticker: str) -> list[dict]:
    raw = getattr(tk, "news", None) or []
    rows = []
    for item in raw[:20]:
        # Older yfinance returns flat dicts; newer nests under "content".
        body = item.get("content") if isinstance(item.get("content"), dict) else item
        link = body.get("link") or body.get("canonicalUrl") or {}
        if isinstance(link, dict):
            link = link.get("url", "")
        rows.append(
            {
                "title": body.get("title") or "",
                "publisher": (
                    body.get("publisher") or (body.get("provider") or {}).get("displayName") or ""
                ),
                "url": link,
                "published": str(body.get("pubDate") or body.get("providerPublishTime") or ""),
            }
        )
    return [r for r in rows if r["title"]]


FETCHERS = {"income": fetch_income, "prices": fetch_prices, "news": fetch_news}


def check() -> int:
    missing = []
    for ticker in TICKERS:
        for dataset in DATASETS:
            path = CACHE_DIR / ticker / f"{dataset}.json"
            if not path.is_file():
                missing.append(f"{ticker}/{dataset}.json  missing")
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                missing.append(f"{ticker}/{dataset}.json  unreadable: {exc}")
                continue
            rows = payload.get("data")
            if not isinstance(rows, list) or not rows:
                missing.append(f"{ticker}/{dataset}.json  no rows")
            else:
                print(f"  ok    {ticker}/{dataset}.json  {len(rows)} rows")

    if missing:
        print("\n" + "\n".join(f"  BAD   {m}" for m in missing))
        return 1
    print(f"\nAll {len(TICKERS) * len(DATASETS)} files present.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", help="one ticker, e.g. AAPL")
    parser.add_argument("--check", action="store_true", help="validate, fetch nothing")
    args = parser.parse_args()

    if args.check:
        return check()

    try:
        import yfinance as yf
    except ImportError:
        print('error: yfinance is missing. Run: pip install -e ".[dev]"', file=sys.stderr)
        return 1

    tickers = (args.only.upper(),) if args.only else TICKERS
    unknown = [t for t in tickers if t not in TICKERS]
    if unknown:
        print(f"error: not in the programme's ticker list: {unknown}", file=sys.stderr)
        return 2

    failures = 0
    for ticker in tickers:
        print(f"\n{ticker}")
        tk = yf.Ticker(ticker)
        for dataset in DATASETS:
            try:
                rows = FETCHERS[dataset](tk, ticker)
                path = write(ticker, dataset, rows)
                print(f"  {dataset:8} {len(rows):5} rows  ->  {path.relative_to(ROOT)}")
            except Exception as exc:  # noqa: BLE001 — report and continue
                failures += 1
                print(f"  {dataset:8} FAILED: {type(exc).__name__}: {exc}")

    print()
    if failures:
        print(f"{failures} dataset(s) failed. Paste the output and we will fix the fetch.")
        return 1
    print("Done. Run --check to validate, then commit cache/ in one commit of its own.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
