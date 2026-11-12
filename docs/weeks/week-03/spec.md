---
kind: build
week: "03"
sprint: "2"
title: Tools are the product
---

## What exists at the end of this week

Three tools over the cached data — income statements, prices and news — each returning a list of
dicts, each refusing any ticker outside `config.TICKERS`, and each carrying a schema that tells
the model what it does and what it accepts.

Nothing calls them in a loop yet. That is next week, and it goes better if these are small.

## Spec

Three modules, one tool each, built in any order. They share a shape, so the first one is the
slow one.

### 1. `src/fin_agent/tools/financials.py`

```python
def get_income_statement(ticker: str, years: int = 3) -> list[dict]:
    """The last `years` annual income statements, newest fiscal year first."""
```

Reads `config.cache_path(ticker, "income")`, takes `payload["data"]`, sorts by `fiscal_year`
descending, and returns the first `years` rows. Each row has exactly these five keys:
`fiscal_year`, `revenue`, `gross_profit`, `operating_income`, `net_income`.

**Missing values stay `None`.** This is the part of the week worth slowing down on. JPM reports
no gross profit and no operating income — banks do not have a cost of goods sold, so the fields
are genuinely absent rather than zero, and the cache holds `null` for all four years. Your tool
must pass that through untouched:

- Not `0`. "Reported as nothing" and "not reported" are different facts, and only one of them is
  true.
- Not dropped. A missing key hides the gap from everything downstream.
- Not derived. Nothing in the file lets you compute it, and an assistant asked to "handle missing
  values" will cheerfully subtract something from revenue.

In week 7 you will ask the agent what JPM's gross margin was. The honest answer is that it does
not report one. Whether you get that answer is decided here, in a tool, four weeks earlier.

Fewer years cached than asked for is not an error: `years=10` returns the four that exist.
`years=0` or negative raises `ValueError`.

### 2. `src/fin_agent/tools/prices.py`

```python
def get_prices(ticker: str, days: int = 30) -> list[dict]:
    """The last `days` trading days of OHLCV data, newest day first."""
```

Reads `config.cache_path(ticker, "prices")`, sorts by `date` descending, returns the first `days`
rows. Keys exactly: `date`, `open`, `high`, `low`, `close`, `volume` — the cached row unchanged,
no rounding and no renaming.

The cache is stored **oldest first**, 500 trading days from 2024-11-01 to 2026-10-30. So "the last
thirty days" is the tail of the file reversed, and a tool that slices from the front returns
November 2024 while sounding entirely confident about it. There is a test for exactly that
mistake because it is the one this tool actually makes.

`days` beyond 500 returns all 500. `days=0` or negative raises `ValueError`.

### 3. `src/fin_agent/tools/news.py`

```python
def get_news(ticker: str, limit: int = 5) -> list[dict]:
    """The `limit` most recent headlines, newest first by publication time."""
```

Reads `config.cache_path(ticker, "news")`, sorts by `published` descending, returns the first
`limit`. Keys exactly: `title`, `publisher`, `url`, `published`.

**The file is not sorted.** For four of the ten tickers the first item is not the newest one —
MSFT leads with 17:31 while its newest is 18:56 — so `data[:limit]` returns the wrong headlines,
and nothing downstream will notice, because the wrong headlines are still real headlines. Sort on
the full `published` timestamp rather than the time of day: CAT's oldest two items are from the
previous date.

The tool does not filter by relevance. AAPL's feed carries Nvidia and TSMC stories, and they come
back. Deciding what is relevant is the agent's job from week 4; a tool that silently drops rows is
a tool whose output you cannot reconcile against its source.

`limit` beyond 10 returns all 10. `limit=0` or negative raises `ValueError`.

### The schemas

Each module also exports a `SCHEMA` — the description the model reads before deciding whether
your tool is the one it wants. Same provider format as week 2's hand-written one:

```python
SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_income_statement",
        "description": "Annual income statement figures for one company, newest year first.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "enum": list(config.TICKERS),
                    "description": "One of the ten tickers this programme covers.",
                },
                "years": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "How many fiscal years to return, newest first.",
                },
            },
            "required": ["ticker"],
        },
    },
}
```

Three things about that, each tested:

`name` matches the function's name exactly. A mismatch is a tool the model asks for and your
registry does not have, and the model has no way to find out why.

Every argument is declared and described, and `required` lists only the ones without defaults.
An undescribed parameter is one the model fills in from its name alone.

`enum` is `list(config.TICKERS)`. Your tool still raises for anything outside the list and always
will — but a refusal the model could have avoided is a wasted call and a confusing trace. Two
expressions of one rule, from one source. Do not retype the ten tickers.

The schema lives beside its function rather than in a shared file, so that week 4 collecting them
is a loop rather than a list somebody has to remember to update.

## Security criterion

Every tool validates its own inputs and rejects any ticker outside `config.TICKERS` with
`ValueError`, including a lowercase one, and the error message names the rejected ticker.

The ticker becomes part of a file path, which makes the allowlist the path control: `AAPL/../JPM`
and `../../.env` have to be refused by the same check, and they are, because membership of a fixed
tuple is not something a traversal string can satisfy. `config.cache_path` already does all of
this, so calling it gives you the guard for free. Reusing one check beats writing a second that
can disagree with it.

Do not normalise. `"aapl"` raises; it is not silently upper-cased. Accepting a near-miss is a
guess about intent, and a tool that guesses is a tool you cannot reason about from its signature.

Next week the pre-tool hook checks the same things centrally, and **both layers stay**. A tool
that is only safe because something upstream protects it is not a safe tool — it is a safe
system, until someone calls the tool directly, which is what your own tests do on line one.

## How it is checked

```bash
pytest tests/week_03
```

151 tests across four files. The three value files assert against the committed cache, so the
expected numbers are exact and there is no judgement about whether you are finished.

`test_financials.py` — 44

- `test_returns_three_years_by_default`, `test_newest_first` — three rows, `[2026, 2025, 2024]`
- `test_googl_is_a_year_behind_aapl` — `[2025, 2024, 2023]`; four of the ten have closed FY2026
  and six have not, so nothing may hard-code "last year"
- `test_exact_field_set`, `test_reads_the_data_key_not_the_envelope` — the five keys, no
  `dataset` or `fetched_at` leaking out of the envelope
- `test_every_ticker_has_at_least_three_years` — all ten, newest first, correct latest year
- `test_aapl_latest_year_values` — the whole FY2026 row, exactly
- `test_msft_latest_revenue`, `test_nvda_oldest_of_three` — exact figures
- `test_amzn_negative_net_income_is_preserved` — FY2022 was a loss; clamping at zero is a lie
- `test_jpm_missing_fields_stay_none` — `gross_profit` and `operating_income` are `None`
- `test_jpm_missing_fields_are_not_zero` — and specifically not `0`
- `test_jpm_keys_are_present_even_when_empty` — all five keys on every row
- `test_jpm_reported_fields_are_intact` — revenue and net income are untouched
- `test_jpm_gross_profit_is_never_derived` — `None` for all four years, not computed
- `test_years_one_returns_only_the_latest`, `test_years_four_returns_four`,
  `test_years_beyond_the_cache_returns_what_exists`, `test_rejects_non_positive_years`
- `test_rejects_ticker_outside_the_list`, `test_rejects_lowercase_ticker`,
  `test_rejects_malformed_ticker`, `test_rejects_path_traversal`,
  `test_error_message_names_the_ticker`

`test_prices.py` — 35

- `test_returns_thirty_rows_by_default`, `test_newest_first`, `test_exact_field_set`
- `test_rows_are_the_cached_rows_unchanged` — compared against the cache file directly
- `test_every_ticker_covers_the_same_window` — 500 rows, 2026-10-30 back to 2024-11-01
- `test_aapl_newest_row` — the whole row; `test_aapl_five_newest_closes`,
  `test_aapl_five_newest_dates`
- `test_thirtieth_row_back` — thirty trading days back is 2026-09-21, not 2026-09-30
- `test_jpm_newest_close`, `test_cat_newest_row`, `test_volume_stays_an_integer`
- `test_days_one_returns_one`, `test_days_beyond_the_cache_returns_what_exists`,
  `test_rejects_non_positive_days`
- `test_does_not_slice_from_the_front` — fails for both the naive slice and the reversed one
- `test_rejects_ticker_outside_the_list`, `test_rejects_lowercase_ticker`,
  `test_rejects_malformed_ticker`

`test_news.py` — 42

- `test_returns_five_items_by_default`, `test_exact_field_set`,
  `test_items_are_the_cached_items_unchanged`
- `test_newest_first_for_every_ticker` — all ten, full list
- `test_msft_newest_item_is_not_the_first_in_the_file` — the exact headline a naive slice misses
- `test_msft_first_three_in_order`, `test_msft_does_not_slice_from_the_front`,
  `test_aapl_newest_item`
- `test_jpm_oldest_item_sorts_last` — an 03:14 item sits ahead of an 11:04 one in the file
- `test_cat_spans_two_days` — sorting on time of day alone gets this ticker wrong
- `test_limit_one_returns_one`, `test_limit_beyond_the_cache_returns_what_exists`,
  `test_every_ticker_has_ten_items`, `test_rejects_non_positive_limit`
- `test_rejects_ticker_outside_the_list`, `test_rejects_lowercase_ticker`,
  `test_rejects_malformed_ticker`
- `test_returns_items_about_other_companies_too` — the Nvidia story in AAPL's feed stays

`test_schemas.py` — 30, parametrised across all three tools

- `test_module_exports_a_schema`, `test_schema_is_a_function_tool`,
  `test_parameters_object_is_well_formed`
- `test_schema_name_matches_the_function`
- `test_schema_has_a_real_description`, `test_function_has_a_docstring`
- `test_parameters_match_the_signature` — declared properties equal the function's arguments
- `test_required_matches_arguments_without_defaults`
- `test_every_parameter_is_described`
- `test_ticker_is_constrained_to_the_programme_tickers` — `enum` equals `list(config.TICKERS)`

## Deliberately not in scope

- **Formatting the return value.** Dexter returns formatted text rather than raw JSON for token
  economy, and we read that this week — but your tools return `list[dict]` and the tests check
  that. Shaping what reaches the model is week 5's size cap, at the hook, once.
- **A fourth tool.** Three is enough to make the loop choose between them next week.
- **Caching, retries, async, or a `Tool` base class.** An assistant adds all four unprompted.
  There is no I/O here worth optimising: the files are local and already in your page cache.
- **A shared `TOOLS` list.** Week 4 assembles it. Building it now means building it twice.
- **Relevance filtering on news.** Week 11, with embeddings, and only after you have seen the
  unfiltered version be a problem.
- **`live=True`.** The signature in `cache/README.md` is a week 10 concern. Cache only.

## Reference reading

Two files, each with one question.

- [`src/tools/finance/`](https://github.com/virattt/dexter) — any one tool file. Look at how much
  of it is the description and the schema rather than the logic. The function bodies in that
  directory are mostly short; the contract around them is not, and the ratio is the week's point.
- `formatters.ts` in the same directory — read it after you have your three tools returning dicts.
  The question to hold: what does it cost, in tokens, to hand a model a JSON array instead of the
  formatted lines this file produces? You are not building it this week, but you will understand
  week 5's size cap faster for having seen what the alternative looks like.
