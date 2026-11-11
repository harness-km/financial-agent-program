---
kind: build
week: "01"
sprint: "1"
title: From workflow to agent
---

## What exists at the end of this week

A working environment — `python scripts/doctor.py` prints PASS on every line — and a submission
post containing five sentences on where three traces from the demo agent diverged, and why.

No code is written this week. That is deliberate. The thing that most reliably derails week 2 is
an environment nobody checked, and the second is a cohort that has never read a trace.

## Spec

Three artifacts, in this order.

### 1. The environment

Work through `docs/program/setup.md` — Path A on your own machine, Path B in Codespaces if your
machine fights you. Then:

```bash
python scripts/doctor.py
```

Every line must read PASS. Post the whole output to the setup thread in Discussions, failures
included. Fifteen minutes of trouble on any single step is the point at which to switch to
Codespaces; that is the documented path, not a retreat.

### 2. Three traces

Run the demo agent on three questions of your own and save all three traces. The demo agent and
its URL are published in the setup thread — you do not need an API key of your own to use it, and
you should not create one this week.

Pick questions that differ in **shape**, not just in subject:

| | A question that needs | Example |
| --- | --- | --- |
| 1 | one lookup | What was NVDA's revenue last year? |
| 2 | two lookups, chained | Has AAPL's gross margin improved since 2023? |
| 3 | a judgement the data does not settle | Is CAT a good business? |

Paste all three traces into your submission post. If a trace is long, attach it as a file rather
than trimming it — the parts people trim are usually the parts worth reading.

### 3. Five sentences

One sentence each, and each has a specific job. This is the deliverable, so write it as prose a
colleague could read, not as notes to yourself.

1. Which tools each run called, and in what order.
2. Where the three paths first diverged from one another.
3. What in the wording of the question caused that divergence.
4. Which run cost the most, and why — read the token counts in the trace rather than guessing.
5. One thing a fixed workflow would have had to do differently to answer question 3 at all.

Sentence 5 is the week's actual point. If you can answer it, you can say what an agent is without
using the word.

## Security criterion

Your clone contains no credential, and you can state in one sentence why `.gitignore` is not a
security control.

The sentence to be able to say out loud: `.gitignore` prevents an accident, not a decision. It
stops you committing `.env` by mistake. It does nothing about a key pasted into a notebook cell, a
prompt or a trace file, and nothing at all once a key has been pushed — at which point the fix is
revoking the key, not deleting the commit.

Nothing in weeks 1 to 3 needs a key, because the committed cache covers it. So the only way to
fail this criterion is to have added a credential you did not need.

## How it is checked

```bash
pytest tests/week_01
```

You write no code this week, so these are the only tests in the programme that pass on a fresh
clone. They check the clone rather than your work. 108 of them, and the parametrised ones name
the exact file when they fail.

`tests/week_01/test_clean_clone.py` — the security criterion:

- `test_repository_is_a_git_checkout` — git is tracking files, since the rest reads its index
- `test_env_is_not_tracked` — no `.env` in `git ls-files`
- `test_env_example_is_tracked` — the template is committed; only the filled-in copy is not
- `test_no_env_file_anywhere_is_tracked` — `.env.local` and friends too
- `test_gitignore_covers` — `.env`, `ledger.csv`, `scratchpad/` and `.runs/` are each listed; the
  ignore for a file has to exist before the week that creates it
- `test_gitignore_is_not_a_security_control` — the week's sentence, written where it cannot be
  skipped: if the ignore list were the control, the scan below would be redundant
- `test_no_credential_in_any_tracked_file` — every tracked file read and checked against six key
  shapes. This is the criterion. In week 7 you grep your own traces for the same thing
- `test_env_example_holds_no_key_values` — any variable ending `_API_KEY` is empty in the template

`tests/week_01/test_environment.py` — the environment and the cache:

- `test_fin_agent_is_importable` — `pip install -e ".[dev]"` ran in this virtual environment
- `test_ten_tickers`, `test_tickers_are_unique_and_upper_case` — `config.TICKERS` is the ten
- `test_cache_path_rejects_an_unknown_ticker` — the guard weeks 2 and 3 inherit rather than rewrite
- `test_cache_holds_exactly_the_programme_tickers` — no extra folder, none missing
- `test_every_file_exists` — thirty files, one case each, so a failure names the file
- `test_every_file_is_a_well_formed_envelope` — the five envelope keys, and `ticker` matching its
  own folder
- `test_every_file_has_the_expected_row_count` — four years, five hundred trading days, ten
  headlines, for all ten tickers
- `test_the_cache_is_not_gitignored` — it is committed on purpose

Then three commands the tests cannot cover, because they are about your machine rather than the
repository:

```bash
python scripts/doctor.py                   # every line PASS
pre-commit run --all-files                 # passes, detect-private-key included
python scripts/refresh_cache.py --check    # all thirty files present and the right shape
```

- `doctor.py` — your Python version, your virtual environment, git, and the pinned tooling
- `pre-commit run --all-files` — the hooks that will police every later commit actually run on
  your machine now, rather than failing for the first time when you are mid-week and in a hurry
- `refresh_cache.py --check` — the same thirty files from the script's own point of view

If a cache test fails on a fresh clone, say so in Blockers before changing anything. A cache that
differs from everyone else's breaks about forty week 3 assertions with no obvious cause.

## Deliberately not in scope

- **Writing code.** Week 2 is the first line of it.
- **Installing an API key.** Not needed until week 4. Adding one now is the only available way to
  fail this week's security criterion.
- **Reading the reference project's source.** Week 2 sends you to one file in it with something
  specific to look for. Browsing it now produces the impression of understanding without any.
- **Fixing a `doctor.py` failure quietly.** Post the output first. Most failures have a known
  one-line answer and somebody else in the cohort has already hit yours.
- **Running `refresh_cache.py` without `--check`.** It would change the numbers every later test
  asserts against. Refreshing the cache is an instructor change, made with the tests in the same
  commit.

## Reference reading

Dexter's README only, and one question to hold the whole way through it: what does this agent
decide at runtime that a workflow decides at build time?

- [`README.md`](https://github.com/virattt/dexter) — the overview and the architecture section.
  Look for where the list of steps stops being in the code. In an n8n canvas that list is the
  canvas; here there is no equivalent picture to point at, and that absence is the whole subject
  of this week.
- Do not open `src/` yet. Week 2 names one file in it and what to look for.
