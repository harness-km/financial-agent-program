# Cached market data

Pre-fetched data for the program's ten tickers, committed to the repository on
purpose.

```text
cache/
└── AAPL/
    ├── income.json
    ├── prices.json
    └── news.json
```

Each file is an envelope rather than a bare array, so the data carries its own
provenance — where it came from and when:

```json
{
  "ticker": "AAPL",
  "dataset": "income",
  "source": "yfinance",
  "fetched_at": "2026-11-11T00:30:00Z",
  "data": [ { "fiscal_year": 2024, "revenue": 0, "gross_profit": 0 } ]
}
```

Your tools read `payload["data"]`. The extra unwrap is deliberate: a number with
no record of where it came from is a number you cannot defend, and that matters
more here than one line of convenience.

## Why this is checked in

Three reasons, and all three are the point rather than a convenience.

Your results match everyone else's. A test can assert that revenue for AAPL
FY2024 is a specific number, which turns "is my tool right?" from a judgement
call into a passing or failing check.

No API keys are needed until week 4, so week 1 is `pip install` and nothing
else.

Nothing flakes mid-demo. Live APIs rate-limit, change shape and go down, and
none of that teaches you anything about agents.

## When you leave the cache

Your tools read from here by default and take `live=True` to fetch fresh data
instead. Week 10 is where that switch starts to matter, because Part 2 works
against the live web and your results stop matching anyone else's — which is a
change in how you verify, not just where the data comes from.

## Refreshing it

`scripts/refresh_cache.py` re-fetches everything from yfinance.

```bash
python scripts/refresh_cache.py --only AAPL    # smoke test one ticker
python scripts/refresh_cache.py                # all ten
python scripts/refresh_cache.py --check        # validate, fetch nothing
```

Do not run the full fetch casually: it changes the numbers the tests assert
against. If the cache needs refreshing, that is an instructor change, with the
tests updated in the same commit. `--check` is safe at any time and is what
`doctor.py` is really asking about.
