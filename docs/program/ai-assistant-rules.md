# Working with your AI coding assistant

You will specify code and direct an assistant to write it. That is the intended
way to work on this course, not a shortcut around it.

Done carelessly it produces code that runs, that you cannot read, and that
breaks in week 6 for reasons seeded in week 3. These rules prevent that. They
apply from week 2 to the end of the program.

## The seven rules

### 1. Give the spec, not the goal

"Build me a financial agent" produces a tangent. A spec produces the thing.

Bad:

> Write me a tool that gets financial data for a stock.

Good:

> Write one function `get_income_statement(ticker: str, years: int = 3)` in
> `src/fin_agent/tools/financials.py`. It reads `cache/{ticker}/income.json`,
> returns a list of dicts newest first with keys `fiscal_year`, `revenue`,
> `gross_profit`, `operating_income`, `net_income`, and raises `ValueError` if
> the ticker is not in `fin_agent.config.TICKERS`. No other functions, no classes.

The weekly `spec.md` is written as a worked example of this. Read it as both the
assignment and the model for how to ask.

### 2. Constrain what it may touch

State the boundary in every prompt: no new dependencies, no refactoring, change
only this function, no classes unless I asked. Reject a large diff without
reading it.

An assistant that quietly improved a neighbouring function has removed your
ability to tell what broke.

### 3. Ask for the approach before the code

> Describe how you would implement this in four sentences, then stop.

This costs one exchange and catches a wrong plan before it becomes a hundred
lines you have to understand in order to reject.

### 4. Never accept code you cannot narrate

If you cannot say out loud what a line does, ask for an explanation or a simpler
version before moving on.

This is the single habit that separates people who finish from people who stall
around week 10. The submission form has a field for anything you could not
explain. Using it honestly is worth more than leaving it blank.

### 5. One change, one run

Never make two changes before running. Two changes means two possible causes,
and you cannot isolate what you never separated.

### 6. Keep a known-good copy

Commit, or save a copy, before any significant change. When an assistant mangles
a working file the fastest route back is the version from twenty minutes ago,
not another prompt.

### 7. Stop after two failures

Two attempts at the same error both failing means stop prompting. Bring it to
the lab hour or the Help category. The third attempt usually widens the damage,
because the model starts rewriting things that were fine.

## Two more for Part 2

A graph fails differently from a loop.

**One node per prompt.** Never let the assistant touch two nodes at once. When a
graph misbehaves you need to know which node produced the bad state.

**Test every node alone before wiring it.** Call it as a plain function with a
hand-made input and check what comes back. A node that is wrong in isolation is
cheap to fix; the same node wrong inside a running graph can cost an evening.

## How to work

Keep VS Code and your assistant in separate windows, and copy code across by
hand.

This is deliberate. Agentic coding tools that edit your files directly will let
you accumulate changes you never looked at, which is precisely the failure these
rules exist to prevent. Code you paste yourself is code you glance at, and that
glance is most of what keeps you oriented.

## One thing to remember about the assistant

It is confident when it is wrong, and it will agree with you when you are wrong.
It has no way of knowing whether its code matches your intent — only whether it
matches your words. That is why the spec does the work, and why the tests are the
arbiter rather than the assistant's own assurance that the code is correct.
