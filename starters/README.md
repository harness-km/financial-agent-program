# Starter notebooks

One notebook per week that builds something, named for its week.

A starter holds no logic. Every line calls something you wrote in
`src/fin_agent/`, and that split is deliberate: logic in a notebook cannot be
tested, and `pytest tests/week_NN` is what decides whether a week is done. If you
find yourself writing a function in a cell, it belongs in the package.

```bash
jupyter notebook starters/week-02.ipynb
```

Or open it in VS Code, which is what the recommended extensions are for. Select
the interpreter inside `.venv` first — `Ctrl+Shift+P`, "Python: Select
Interpreter" — or the imports will fail while the same code passes in the
terminal.

## What a starter is for

The assignment is `docs/weeks/week-NN/spec.md`. Read that first, write the
modules, run the tests. The notebook is where you put the pieces together once
they pass, and where you look at the things the tests cannot show you — the
actual request body, the raw response, the shape of what the model sent back.

Several cells are deliberately empty, marked `TODO`. Those are the parts the spec
asks you to write by hand rather than copy: the tool schema in week 2, the system
prompt, the cost arithmetic. A starter that filled them in would be answering the
assignment.

## Outputs are stripped on commit

`nbstripout` runs as a pre-commit hook, so what you push is the code you wrote
rather than the numbers it produced. That is intentional — a notebook full of
other people's outputs is unreadable in a diff, and it is a good way to commit a
key you printed while debugging.

Put the numbers in your pull request instead, where the ledger table and the eval
score are meant to go.

## Week 1 has no starter

Week 1 writes no code. Its checks are `pytest tests/week_01` and three commands
against your machine, all in its spec.
