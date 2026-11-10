---
kind: build
week: "00"
sprint: "0"
title: Short focus phrase
---

Copy this folder to `week-NN/` and fill it in. Everything below the frontmatter
becomes the GitHub issue body verbatim, so write it for the person doing the
work, not for a parser.

Keep the six headings and their order. `scripts/seed_issues.py` does not require
them, but the cohort relies on finding the same sections in the same places.

## What exists at the end of this week

The observable result, not the activity. One or two sentences.

Good: "A function that returns the last three income statements for any of the
ten tickers, as a list of dicts."

Not: "Understanding of how tools work."

## Spec

Precise enough to prompt from without inventing anything. Function names,
signatures, file paths, return shapes, error behaviour.

```python
def example(ticker: str, years: int = 3) -> list[dict]:
    ...
```

State what the function must raise and when. An assistant will invent an answer
to any question you leave open, and you will not notice until week 6.

## Security criterion

What the code must do, worded so it can pass or fail. Not a topic.

Good: "Rejects any ticker outside `config.TICKERS` with `ValueError`."

Not: "Consider input validation."

From week 4 this usually means adding a policy to the pre-tool or post-tool
hook rather than writing a new mechanism. Say which hook and what it enforces.

## How it is checked

```bash
pytest tests/week_NN
```

Then list what each test asserts, in one line each, so the spec and the tests
cannot drift apart without somebody noticing.

- `test_x` — returns three years for AAPL, newest first
- `test_y` — raises on an unknown ticker

## Deliberately not in scope

What not to build this week. This section exists because an assistant will
cheerfully add caching, retries, async and a class hierarchy nobody asked for,
and because next week's work depends on this week's code being small.

## Reference reading

Which files in the reference project to read, and what to look for in them. A
file path with no reason attached does not get read.

- `src/agent/agent.ts` — the class docstring states the whole design in five
  lines
