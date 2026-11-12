# How work happens here

These conventions are part of the curriculum, not bureaucracy. They are what
makes thirty people's work readable by each other.

If you have never used GitHub, start with [`docs/program/github.md`](docs/program/github.md)
instead — it covers the same ground from the beginning, with the reasoning for
each step. This file is the short version, for reference once you are going.

## One source of truth

Dependencies live in `pyproject.toml` only. There is no `requirements.txt`,
deliberately: two dependency files drift, and the first thing that breaks is
somebody else's environment.

The same principle applies to the backlog. Each week's spec lives in
`docs/weeks/week-NN/spec.md`, and the GitHub issue is generated from it by
`scripts/seed_issues.py`. Edit the spec, not the issue.

## Where the copies are

You work in your own fork, never in the course repository. Nothing you do can
affect anyone else's copy, which is deliberate — it means you can experiment
freely.

| Name | What it is |
| --- | --- |
| `upstream` | the course repository. Where each week's material comes from |
| `origin` | your fork on GitHub. Where your own work is backed up |
| your clone | the folder on your laptop. Where you actually work |

## Branches in the course repository

| Branch | Holds |
| --- | --- |
| `main` | every week released so far — specs, tests, starters |
| `week-NN-content` | a week being written. It appears on `main` when that week opens |
| `week-NN-start` | a complete working version of everything up to week N |

Material arrives weekly rather than all at once, so pull at the start of each
week:

```bash
git pull upstream main
```

If you miss a week, take the code you are missing without disturbing your own:

```bash
git fetch upstream
git checkout upstream/week-NN-start -- src/fin_agent/
```

The `week-NN-start` branches are maintained by the instructor. Read them, copy
from them, compare them against your own — but there is nothing to commit to
them, since you have no write access to that repository.

## Branches in your own fork

Up to you, and genuinely so. Some people keep everything on `main`; some make a
branch per week:

```text
week-04
```

There is no pull request to open and nothing to merge, so the only person your
branching scheme has to suit is you.

## Commits

[Conventional Commits](https://www.conventionalcommits.org/). The type matters
more than the formatting:

```text
feat(tools): add income statement tool
fix(agent): stop loop re-calling the same tool
docs(week-05): add compaction spec
test(week-03): assert revenue for AAPL FY2024
chore: bump ruff
```

Write the message for yourself in three months, looking for the version that
worked. "stuff" will not help you.

Commit and push at the end of every session at least:

```bash
git add .
git commit -m "week 2: tool call working"
git push
```

Ten seconds, and it is the difference between a bad week and a lost term.

## Submissions

Nothing is marked and nothing is reviewed by the instructor. Each week you post
what you did in the **Submissions** category in Discussions, and the cohort
reads it.

The form asks for your spec, your prompts, your cost ledger row and what broke.
Post the prompts that went wrong — the Definition of Done calls the prompt trail
the item carrying the most weight, and it means it.

Every item is in [`docs/program/definition-of-done.md`](docs/program/definition-of-done.md),
and all six are things you check yourself.

## Reading each other's work

Read somebody else's submission before posting your own. You are not reading for
correctness — the tests do that. You are reading the spec and the prompt trail,
which is where the understanding shows.

Three useful questions: does the spec describe what was actually built, could
you follow those prompts yourself, and is there a line in there nobody could
explain out loud.

## Keeping notebooks clean

`nbstripout` runs as a pre-commit hook and strips notebook outputs before they
are committed. That is on purpose: a notebook full of other people's outputs is
unreadable, and printed output is a good way to commit a key by accident.

```bash
pre-commit install
```

Run that once, after installing the package. The numbers your notebook produced
belong in your submission post, not in the file.

## Code

- Logic goes in `src/fin_agent/`. Notebooks import it and call it.
- Public functions get a docstring saying what they return, because from week 3
  the agent reads those docstrings too.
- No secrets in code, ever. Keys come from the environment.
