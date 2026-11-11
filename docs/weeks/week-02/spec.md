---
kind: build
week: "02"
sprint: "1"
title: What an LLM does, and how to direct one
---

## What exists at the end of this week

Four small modules: one that makes a single raw model call, one that parses what came back and
decides whether to honour it, one tool for it to call, and a cost ledger. Together they answer
"what is the latest close for AAPL?" without a framework anywhere in the stack.

The deflation this week turns on is that the model never calls a tool. It emits JSON asking for
one, and `dispatch.py` decides. Everything in weeks 4 to 16 is a bigger version of that decision.

## Spec

Four files. Build them in this order — each is testable before the next exists.

### 1. `src/fin_agent/tools/quote.py`

```python
def get_latest_close(ticker: str) -> float:
    """The most recent closing price for one of the program's tickers."""
```

Reads `config.cache_path(ticker, "prices")`, takes `payload["data"]`, and returns the `close` of
the row with the newest `date`. Do not assume the file is sorted — sort it.

Note what you did *not* write: the ticker check. `config.cache_path` already raises `ValueError`
for anything outside `config.TICKERS`, so calling it gives you the guard for free. Reusing one
check is better than writing a second one that can disagree with it.

### 2. `src/fin_agent/llm.py`

```python
def call_model(messages: list[dict], tools: list[dict]) -> dict:
    """POST one chat completion request and return the decoded JSON unchanged."""
```

About fifteen lines. `requests.post` to the provider's chat completions endpoint, `config.MODEL`
as the model, `messages` and `tools` passed straight through, `response.raise_for_status()`, then
`response.json()` returned **unmodified**. No retries, no streaming, no helper classes, no
parsing — parsing is the next file's job and keeping them apart is the point.

Read the API key from `os.environ["OPENAI_API_KEY"]` inside the function. It is not a parameter.
Raise `RuntimeError` with a readable message if it is unset.

`tools` is the schema you hand-write for `get_latest_close` — one dict, in the provider's function
format, with a name, a one-line description and a `ticker` parameter. Write it by hand once. In
week 3 you will see what a vague description does to a model's behaviour, and it lands harder if
you wrote a good one first.

### 3. `src/fin_agent/dispatch.py`

```python
@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict


def parse_tool_call(response: dict, allowed: Collection[str]) -> ToolCall | None:
    """Pull one validated tool call out of a raw model response."""


def run_tool_call(call: ToolCall, registry: Mapping[str, Callable[..., object]]) -> str:
    """Invoke the named tool and return its result as a string."""
```

`parse_tool_call`, in order:

| Condition | Result |
| --- | --- |
| `response["choices"][0]["message"]` missing, or not a dict | `ValueError` |
| no `tool_calls`, or it is `None` or empty | `None` — the model answered in prose, which is allowed |
| the first call's `function.name` is not in `allowed` | `ValueError` |
| `function.arguments` is not valid JSON | `ValueError` |
| the parsed arguments are not a JSON object | `ValueError` |
| otherwise | `ToolCall(name, arguments)` |

Only the first entry of `tool_calls` is handled. Parallel tool calls are week 4's problem.

`run_tool_call` raises `ValueError` if `call.name` is not in `registry`, otherwise returns
`str(registry[call.name](**call.arguments))`. An argument the tool does not accept raises
`TypeError` from Python itself — let it. The tool does not run, which is the behaviour you want;
week 4 is where every refusal gets one name and one place to live.

`allowed` and `registry` look redundant this week and are not. `allowed` is what the model is
permitted to ask for; `registry` is what your process is willing to execute. In week 4 those two
checks become the pre-tool hook, and keeping them separate now is why that is a small change.

### 4. `src/fin_agent/ledger.py`

```python
LEDGER_HEADER = (
    "timestamp",
    "week",
    "model",
    "calls",
    "tokens_in",
    "tokens_out",
    "cost_usd",
    "note",
)


def log_run(
    *,
    week: str,
    model: str,
    calls: int,
    tokens_in: int,
    tokens_out: int,
    cost_usd: float,
    note: str = "",
    path: Path | None = None,
) -> Path:
    """Append one row to the cost ledger and return the file it was written to."""
```

Writes CSV to `path or config.LEDGER_PATH`, creating the file with `LEDGER_HEADER` as its first
row if it does not exist and appending otherwise. `timestamp` is UTC, ISO-8601, to the second.
Returns the path. Keyword-only arguments, on purpose: four integers in a row is exactly the
signature an assistant fills in the wrong order.

`ledger.csv` is gitignored, so the file stays yours. The row goes in the cost ledger table in your
pull request. Take `tokens_in` and `tokens_out` from `response["usage"]` —
`prompt_tokens` and `completion_tokens` — and work `cost_usd` out by hand from the provider's
published price. Doing that arithmetic once, manually, is worth more than a lookup table.

### Putting it together

In your notebook: build `messages` and `tools`, call `call_model`, `parse_tool_call` the response
with `allowed={"get_latest_close"}`, `run_tool_call` it with
`registry={"get_latest_close": get_latest_close}`, then `log_run` the usage figures. Expect a
float somewhere near 344.63.

If you have no model key this week, run the same four steps against
`tests/fixtures/model/tool_call.json` instead of a live response, and say so in your pull request.
The parsing, dispatch and ledger code is identical either way; only `call_model` is skipped.

## Security criterion

Your code validates the model's output before acting on it, and fails closed on everything it does
not recognise — and the API key is never a value your code passes around.

Three things, all of them checkable:

1. `parse_tool_call` raises `ValueError`, rather than returning a default or a guess, for an
   unrecognised response shape, a tool name outside `allowed`, arguments that are not valid JSON,
   and arguments that are not a JSON object.
2. `run_tool_call` refuses any name that is not in `registry`.
3. `call_model` reads `OPENAI_API_KEY` from the environment inside the function. No parameter of
   any function you write this week takes a key, token or secret.

Item 3 is narrower than it looks. A key that is a parameter is a key that ends up in a notebook
cell, in a prompt you paste into Discussions, and in week 7 in every trace file. Keeping it out of
your own signatures is what makes the week 7 criterion — grep your traces, find nothing — possible
rather than aspirational.

This is also last week's sentence made executable. If your code is what decides, your code is the
control, and the model's output is input from an untrusted source: it is downstream of everything
the model has read.

## How it is checked

```bash
pytest tests/week_02
```

`tests/week_02/test_quote.py`

- `test_latest_close_aapl` — returns `344.63` for AAPL
- `test_latest_close_jpm` — returns `337.04` for JPM
- `test_latest_close_cat` — returns `622.75` for CAT
- `test_latest_close_is_a_float` — a `float`, not a string and not the row it came from
- `test_latest_close_for_every_ticker` — all ten, each from the 2026-10-30 row
- `test_latest_close_takes_the_newest_row_not_the_first` — the cache is oldest-first, so
  `data[0]` would be a November 2024 price
- `test_latest_close_rejects_unknown_ticker` — `ValueError` for `TSLA`
- `test_latest_close_rejects_lowercase` — `ValueError` for `aapl`; the list is exact
- `test_latest_close_rejects_empty_ticker` — `ValueError` for `""`
- `test_latest_close_rejects_path_traversal` — `ValueError` for `AAPL/../JPM` and two others

`tests/week_02/test_dispatch.py`

- `test_parses_a_tool_call` — returns `ToolCall("get_latest_close", {"ticker": "AAPL"})`
- `test_arguments_are_a_dict_not_a_string` — the provider's JSON string is decoded
- `test_tool_call_is_frozen` — `ToolCall` cannot be mutated after validation
- `test_returns_none_for_a_prose_answer` — a response with no `tool_calls` gives `None`
- `test_rejects_unknown_tool_name` — `ValueError` when the name is outside `allowed`
- `test_rejects_unparseable_arguments` — `ValueError` when `arguments` is not valid JSON
- `test_rejects_non_object_arguments` — `ValueError` when `arguments` decodes to a list
- `test_rejects_unrecognised_shape` — `ValueError` for five malformed responses
- `test_empty_allowed_set_permits_nothing` — an empty allowlist permits nothing
- `test_run_tool_call_returns_a_string` — dispatches and stringifies the result
- `test_run_tool_call_rejects_unregistered_name` — `ValueError` for a name not in `registry`
- `test_run_tool_call_propagates_tool_validation` — the tool's own `ValueError` reaches the caller
- `test_run_tool_call_does_not_run_an_unregistered_tool` — the refused tool is never invoked
- `test_call_model_takes_no_credential_argument` — no parameter of `call_model` is named for a
  key, token or secret
- `test_no_function_in_llm_or_dispatch_takes_a_credential` — the same rule across both modules

`tests/week_02/test_ledger.py`

- `test_ledger_header_is_the_agreed_columns` — the eight columns, in order
- `test_ledger_creates_file_with_header` — first call writes `LEDGER_HEADER`, then one row
- `test_ledger_returns_the_path_it_wrote` — returns the path, so a caller can report it
- `test_ledger_appends_without_repeating_header` — second call adds a row, header stays once
- `test_ledger_row_round_trips` — every value reads back through `csv.DictReader` unchanged
- `test_ledger_timestamp_is_iso8601` — the timestamp parses with `datetime.fromisoformat`
- `test_ledger_note_with_a_comma_survives` — use the `csv` module; an f-string breaks here
- `test_ledger_arguments_are_keyword_only` — positional arguments raise `TypeError`

Before you start, `pytest tests/week_02` stops at collection with a `ModuleNotFoundError` naming
the module you have not written yet. That is the correct first result, not a broken test file —
and the error names the file to create next, in the order above.

## Deliberately not in scope

- **Any loop.** One call, one parse, one dispatch, then stop. Week 4 is the loop, and it is much
  easier to write around code that does exactly one turn.
- **A framework.** No LangChain this week, even though it is installed. You cannot judge what it
  does for you until you have done it once without it.
- **Retries, backoff, timeouts or streaming.** One `requests.post`.
- **More than one tool.** Week 3 builds three properly. A second one now gets built twice.
- **Parallel tool calls.** Take `tool_calls[0]` and ignore the rest.
- **A price table or a cost calculator.** Work the cost out by hand and pass the number in.
- **Pydantic models for the response.** A frozen dataclass and four `if` statements. The point of
  this week is seeing the validation, and a library does it where you cannot watch.
- **Committing `ledger.csv`.** It is gitignored. The row belongs in your pull request.

## Reference reading

One file, and one question for each half of it.

- [`src/agent/tool-executor.ts`](https://github.com/virattt/dexter) — read only as far as where a
  tool call is looked up and invoked. Look for how many distinct things happen between "the model
  asked for this" and "the function ran": a name resolved, arguments checked, approval considered,
  a result shaped. Your `parse_tool_call` plus `run_tool_call` is the two-function version of that
  file, and in week 4 it grows toward it.
- Then the same file's handling of a tool the model named but the executor does not have. Compare
  it with your `ValueError`. There is no third option that is safe: you either refuse, or you hand
  the model something it will treat as an answer.

Do not read `src/agent/agent.ts` yet. The loop is two weeks away, and knowing how it ends makes
the dispatch code look like a formality rather than the control it actually is.
