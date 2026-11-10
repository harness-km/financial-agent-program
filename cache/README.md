# Cached market data

Pre-fetched data for the program's ten tickers, committed to the repository on
purpose.

```
cache/
└── AAPL/
    ├── income.json
    ├── prices.json
    └── news.json
```

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

`scripts/refresh_cache.py` re-fetches everything from yfinance and SEC EDGAR.
Do not run it casually: it changes the numbers the tests assert against. If the
cache needs refreshing, that is an instructor change, with the tests updated in
the same commit.
