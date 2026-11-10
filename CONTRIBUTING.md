# Contributing

How work gets into this repository. These conventions are part of the
curriculum, not bureaucracy — they are what makes thirty people's work
reviewable by each other.

## One source of truth

Dependencies live in `pyproject.toml` only. There is no `requirements.txt`,
deliberately: two dependency files drift, and the first thing that breaks is
somebody else's environment.

The same principle applies to the backlog. Each week's spec lives in
`docs/weeks/week-NN/spec.md`, and the GitHub issue is generated from it by
`scripts/seed_issues.py`. Edit the spec, not the issue.

## Branches

One branch per week's assignment, named for the week:

```
week-04-<your-github-handle>
```

The `week-NN-start` branches are reference starting points maintained by the
instructor. Do not commit to them.

## Commits

[Conventional Commits](https://www.conventionalcommits.org/). The type matters
more than the formatting:

```
feat(tools): add income statement tool
fix(agent): stop loop re-calling the same tool
docs(week-05): add compaction spec
test(week-03): assert revenue for AAPL FY2024
chore: bump ruff
```

Write the message for the person reviewing it, who is a peer with no context on
your afternoon.

## Pull requests

One pull request per week, against `main`, using the template. It must:

- pass `pytest tests/week_NN`
- pass `ruff check .` and the markdown linter
- include your prompt trail
- include your cost ledger row
- link the week's issue with `Closes #NN`

Keep notebook outputs out of the diff. `nbstripout` runs as a pre-commit hook
for exactly this reason — a pull request full of base64 image blobs cannot be
reviewed.

```bash
pre-commit install
```

## Reviews

Review someone else's pull request before asking for one on yours. You are not
reviewing for correctness — the tests do that. You are reviewing the spec and
the prompt trail, which is where the understanding shows.

Three useful questions: does the spec describe what was actually built, could
you follow the prompts yourself, and is there a line in here nobody could
explain out loud.

## Code

- Logic goes in `src/fin_agent/`. Notebooks import it and call it.
- Public functions get a docstring saying what they return, because the agent
  reads those docstrings too.
- No secrets in code, ever. Keys come from the environment.
