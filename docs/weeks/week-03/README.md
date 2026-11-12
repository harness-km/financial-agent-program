# Week 3 — Tools are the product

Sprint 2, first week. No consultant session until the end of week 4.

## What changes this week

At the end of week 2 the model could call one tool that returned a single float. At the end of
this week it has three, over income statements, prices and news, each describing itself well
enough that the model can choose between them.

The shift is in where you think the work is. A tool is a few lines of file reading wrapped in a
contract — a name, a description, a parameter schema, a return shape, and a rule about what it
refuses. The contract is most of it, and the contract is what the model actually consumes.

## Why it is in this order

Next week the loop chooses which tool to call, and a loop is far easier to debug when the things
it calls are already known-good. The three tools are also what makes next week's loop
interesting: with one tool there is no choosing, and the iteration cap has nothing to bite on.

It sits after week 2 because you need to have seen the raw request to understand what a schema
is for. The schema is not configuration — it is text you are writing into the model's context,
and week 2 is where you saw that context as JSON on your screen.

## The session

A tool built live against the cache, from nothing to passing tests, then the same tool given a
vague one-line description and run again. Watch it get called for the wrong question, with the
wrong arguments.

That misuse is the lesson twice over. It is a quality problem — the model cannot pick well from a
bad description — and it is the security problem, because a tool with a loose contract is one
that gets called in ways you did not plan for. Those are the same defect seen from two angles,
which is why this course has no separate security session.

Then ten minutes on Dexter's formatters and token economy: what it costs to hand a model raw JSON
rather than formatted lines, and why that becomes week 5's problem rather than this week's.

## What you will have afterwards

- `src/fin_agent/tools/financials.py`, `prices.py` and `news.py`, each with a `SCHEMA`
- 151 passing tests: `pytest tests/week_03`
- Your cost ledger row and your prompt trail, as every week

No consultant section this week — sprint 2's increment is due at the end of week 4, and it
reasons about the loop and these tools together.

See [`spec.md`](spec.md) for the signatures, the exact return shapes and what each test asserts.

## If you are behind

Write one tool completely before starting the next. They share a shape, so the first costs most
of the time and the other two follow quickly — and `pytest tests/week_03/test_financials.py`
gives you something green a third of the way in.

Two things to get right rather than fast, because both are silent when wrong:

**JPM's missing fields stay `None`.** Not `0`, not dropped, not computed. Banks report no gross
profit, and five tests exist for this one fact.

**Sort before you slice.** The price cache is oldest-first and the news cache is not sorted at
all, so taking the first rows of either gives you plausible, wrong, confident data.

If you only finish one tool, make it `financials.py`. Week 4's demo question needs income
statements, and week 7's hallucination case is JPM's gross margin.
