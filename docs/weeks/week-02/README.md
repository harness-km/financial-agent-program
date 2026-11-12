# Week 2 — What an LLM does, and how to direct one

Sprint 1. The sprint boundary falls at the end of this week, so the consultant
session follows the build session.

## What changes this week

At the start of the week you have an environment. At the end you have four small
modules that answer "what is the latest close for AAPL?" with no framework
anywhere in the stack: one that makes a single raw model call, one that parses
what came back and decides whether to honour it, one tool for it to call, and a
cost ledger.

The thing that changes in your head is smaller and more useful. The model never
calls a tool. It emits JSON asking for one, and your code decides. Everything in
weeks 4 to 16 is a larger version of that decision, and the security criterion
from week 4 onward is a policy attached to the place where it gets made.

## Why it is in this order

This is the only week where you see the raw request and the raw response with
nothing in between. From week 3 there are proper tools, from week 4 a loop, from
week 6 a prompt assembled out of markdown files — each one a layer between you and
the exchange. You cannot judge what a framework does for you until you have done
it once without one, and after this week you never have to again.

It is also why validation is this week's security criterion rather than a later
one. Once you have seen that your code is what honours or refuses the model's
request, "the model's output is untrusted input" stops being a slogan.

## The session

First hour: tokens, context window, temperature, and the deflation above. Then the
raw HTTP call built live, about fifteen lines, with the response printed in full
so everyone sees the actual shape of `tool_calls`.

Second hour: directing an assistant. A vague prompt produces a hundred lines of
invented abstractions; a spec-based prompt produces the thing. The seven rules in
[`ai-assistant-rules.md`](../../program/ai-assistant-rules.md) start here and
apply for the rest of the programme.

Then the cost ledger, and why an agent's cost is a design property rather than an
accounting detail.

The consultant session follows: sprint 1's increment reasons about *a model that
can call one tool* — vendor dependency, what data leaves the firm, who holds the
keys, own versus rent. First sprint review and first retrospective.

## What you will have afterwards

- `src/fin_agent/tools/quote.py`, `llm.py`, `dispatch.py` and `ledger.py`
- 48 passing tests: `pytest tests/week_02`
- A cost ledger row in your submission post — model, calls, tokens in and out, cost
- Your prompt trail, including the prompts that went wrong
- Sprint 1's consultant-track section, following
  [`plan-template.md`](../../consultant/plan-template.md)

See [`spec.md`](spec.md) for the signatures, the error behaviour and what each
test asserts.

You do not need a model API key this week. If you have one, make the live call. If
you do not, run the same parse-dispatch-ledger path against
`tests/fixtures/model/tool_call.json` and say so in your submission post — the
only part you skip is `call_model` itself.

## If you are behind

Write the four files in the order the spec gives them, and run the tests after
each one rather than at the end. Each test file maps to one module, so you get
something green three times instead of once:

```bash
pytest tests/week_02/test_quote.py       # after quote.py        — 21 pass
pytest tests/week_02/test_ledger.py      # after ledger.py       —  8 pass
pytest tests/week_02/test_dispatch.py    # after llm + dispatch  — 19 pass
```

Before you start, `pytest tests/week_02` stops at collection with a
`ModuleNotFoundError` naming the module you have not written yet. That is the
correct first result, not a broken test file.

The one piece week 3 cannot route around is `dispatch.py`. Week 3's three tools
are called through it, week 4 wraps hooks around it, and every later week's
security criterion lands on that boundary. If you run out of time, get that one
right and come back for the ledger.
