# Start here

Everything you need to do before week 1, in order, with nothing in it you can
safely skip.

Work down the list. Each step is marked one of two ways:

- 📖 **Read only** — nothing to do but read. No commands, no accounts, no
  installing.
- ⚙️ **Action required** — you do something, and the step tells you how to check
  it worked.

Budget about two hours in total, and there is no prize for doing it in one
sitting. Steps 1 to 4 are reading and can be done on a phone on a Tuesday
evening; steps 5 onwards want you at your laptop.

If a step fights you for fifteen minutes, stop and post it in the **Blockers**
category in Discussions. That is the documented path, not a last resort. We also
do all of this together in the setup session, so arriving with it half-finished
and a list of questions is a perfectly respectable plan.

## At a glance

| # | Step | | Time |
| --- | --- | --- | --- |
| 1 | [What this course is](#1--what-this-course-is) | 📖 | 10 min |
| 2 | [How a week works](#2--how-a-week-works) | 📖 | 10 min |
| 3 | [What "finished" means](#3--what-finished-means) | 📖 | 5 min |
| 4 | [Git and GitHub, from scratch](#4--git-and-github-from-scratch) | 📖 | 20 min |
| 5 | [Make a GitHub account](#5--make-a-github-account) | ⚙️ | 10 min |
| 6 | [Fork the course repo](#6--fork-the-course-repo) | ⚙️ | 2 min |
| 7 | [Install Python, Git and VS Code](#7--install-python-git-and-vs-code) | ⚙️ | 20 min |
| 8 | [Clone your fork and open it](#8--clone-your-fork-and-open-it) | ⚙️ | 10 min |
| 9 | [Learn your way around VS Code](#9--learn-your-way-around-vs-code) | 📖 | 20 min |
| 10 | [Create the environment](#10--create-the-environment) | ⚙️ | 15 min |
| 11 | [Run the check script](#11--run-the-check-script) | ⚙️ | 5 min |
| 12 | [Set up your AI assistant](#12--set-up-your-ai-assistant) | ⚙️ | 10 min |
| 13 | [Say hello in Discussions](#13--say-hello-in-discussions) | ⚙️ | 5 min |
| 14 | [Run week 1's tests](#14--run-week-1s-tests) | ⚙️ | 5 min |

Two things that are explicitly **not** on this list, so you can stop worrying
about them: you do not need an API key until week 4, and you do not need to know
any Python before week 1.

---

## 1 · What this course is

📖 **Read only**

Read the [`README.md`](README.md) in this folder, top to bottom. It is short.

Then read the outline for the half you are starting:
[`docs/program/part-1-outline.md`](docs/program/part-1-outline.md) — weeks 1 to
8, where you build a single financial-analyst agent.

**Why first.** Everything after this makes more sense once you know what you are
building. Skipping to the installing is the most common way to spend an hour
setting up tools for a course you have not understood yet.

## 2 · How a week works

📖 **Read only**

Read [`docs/program/sprint-plan.md`](docs/program/sprint-plan.md).

The shape: two-week sprints, a build session each week, and a consultant session
every second week that asks what it would take for a real firm to actually run
what you just built. Material is published week by week rather than all at once,
which is why step 4 matters.

## 3 · What "finished" means

📖 **Read only**

Read [`docs/program/definition-of-done.md`](docs/program/definition-of-done.md).

Six items, every week, all of them checked by you. Nothing here is marked and
nobody reviews your work — which makes this document the only definition of
"done" you get, so it is worth the five minutes now rather than discovering it in
week 3.

The item that surprises people: your prompt trail carries the most weight. Not
the working code. Start keeping your prompts from the first thing you build.

## 4 · Git and GitHub, from scratch

📖 **Read only**

Read [`docs/program/github.md`](docs/program/github.md).

If you have never used GitHub, read all of it — it assumes nothing, explains why
each command exists, and has a diagram of the three copies of this course that
will save you a lot of confusion later. If you use GitHub daily, skim the
branches section and move on.

**Read it before doing steps 5, 6 and 8**, which are the same steps with the
explanations stripped out. You will not retain the reasoning if you do the
clicking first.

## 5 · Make a GitHub account

⚙️ **Action required**

1. Go to [github.com](https://github.com) and sign up. Free, no card.
2. Pick a username you would not mind a future employer seeing.
3. Turn on two-factor authentication now: **Settings → Password and
   authentication → Two-factor authentication**. An authenticator app on your
   phone is simplest.

**Check it worked.** You can sign out and sign back in, and it asks for a code.

**Why 2FA now.** GitHub requires it and will eventually force the issue. Two
minutes today, or locked out mid-week later.

Already have an account? Use it. Skip to step 6.

## 6 · Fork the course repo

⚙️ **Action required**

1. Open [the course repo](https://github.com/harness-km/financial-agent-program).
2. Click **Fork**, top right.
3. Click **Create fork**.

**Check it worked.** You have a repo at
`github.com/<your-username>/financial-agent-program`, and the page says "forked
from harness-km/financial-agent-program" under the title.

**Why.** You cannot write to the course repo, which is what stops thirty people
overwriting each other. Your fork is your own copy, and your work lives there.

## 7 · Install Python, Git and VS Code

⚙️ **Action required**

Follow step 1 of [`docs/program/setup.md`](docs/program/setup.md) — three
downloads with versions.

**On Windows, tick "Add python.exe to PATH" in the Python installer.** Nearly
every Windows setup problem on this course traces back to that one checkbox, and
it is easier to tick now than to diagnose later.

**Check it worked.** Open a *new* terminal and run:

```bash
python --version
git --version
```

Python must report 3.12 or later. On macOS use `python3`. If either command is
not found, fix that before step 8 — nothing downstream will work.

Your machine blocks installing software? Skip to Path B in
[`docs/program/setup.md`](docs/program/setup.md) and use Codespaces, which runs
in a browser. It is a fully supported path, not a lesser one.

## 8 · Clone your fork and open it

⚙️ **Action required**

In a terminal, in whatever folder you keep projects, with **your own username**
in the first line:

```bash
git clone https://github.com/<your-username>/financial-agent-program.git
cd financial-agent-program
git remote add upstream https://github.com/harness-km/financial-agent-program.git
code .
```

**Check it worked.**

```bash
git remote -v
```

Four lines: `origin` and `upstream`, each twice. `origin` must have *your*
username in it. If it says `harness-km`, you cloned the course repo instead of
your fork — delete the folder and run the clone again with your own address.

**Why the third line.** Your clone knows about your fork and nothing else. That
line introduces it to the course repo, which is where each week's material comes
from. Without it there is no way to collect week 2.

VS Code opens and asks whether you trust the authors. Yes — it is your own clone
of a repository you just looked at. It then offers to install the recommended
extensions. Accept.

## 9 · Learn your way around VS Code

📖 **Read only**

Read [`docs/program/vscode.md`](docs/program/vscode.md).

Four things: open a folder rather than a file, use the terminal, pick the right
Python, and run a notebook. The third one causes more confusion on this course
than the other three together, and step 10 is where you will need it.

## 10 · Create the environment

⚙️ **Action required**

Follow step 3 of [`docs/program/setup.md`](docs/program/setup.md). In short, in
the VS Code terminal:

```bash
python -m venv .venv
```

Activate it — pick the line for your machine:

```bash
.venv\Scripts\activate          # Windows PowerShell
source .venv/bin/activate       # macOS / Linux
```

Then install:

```bash
pip install -e ".[dev]"
pre-commit install
```

Finally, point the editor at the same Python: `Ctrl+Shift+P`, then
**Python: Select Interpreter**, then the entry with `.venv` in its path.

**Check it worked.** Three things. Your prompt starts with `(.venv)`. The
bottom-right of VS Code shows `.venv` when a Python file is open. And this prints
a version rather than an error:

```bash
python -c "import fin_agent; print('ok')"
```

**Why a virtual environment.** It keeps this course's packages in a folder inside
the project instead of mixed into your system Python, so nothing here can break
anything else on your machine. `.venv` is ignored by git — it never leaves your
laptop.

**Why select the interpreter separately.** The terminal and the editor make the
choice independently. Do only the first and your tests pass in the terminal while
the editor underlines your imports in red, which is a genuinely maddening
afternoon.

## 11 · Run the check script

⚙️ **Action required**

```bash
python scripts/doctor.py
```

**Check it worked.** Every line reads PASS.

If any line fails, that line names what is missing. The troubleshooting section
at the bottom of [`docs/program/setup.md`](docs/program/setup.md) covers the
common ones. Still stuck after fifteen minutes: post the **whole** output in
Blockers, not a summary — the useful detail is almost always in the line people
trim out.

**Why a script.** Setup fails in about nine ways, and asking a script is faster
than reading nine pages to find out which one you hit.

## 12 · Set up your AI assistant

⚙️ **Action required**

Read [`docs/program/assistant.md`](docs/program/assistant.md), then:

1. Open Claude, Gemini or ChatGPT in a browser and sign in. A free tier is fine
   to start.
2. Keep it in a **separate window** from VS Code. Not a plugin, not side by side
   in the editor.

**Check it worked.** You can type a question into it and read the answer without
touching VS Code.

**Why separate windows.** It is the one non-obvious rule of this course and the
guide explains it properly: tools that write into your files directly let you
accumulate hundreds of lines you have never read, and then week 6 breaks for a
reason planted in week 3. Copying code across by hand means you glance at it, and
that glance is most of what keeps you oriented over sixteen weeks.

This is not your agent's API key. That is a different account with a different
bill, and you do not need it until week 4.

## 13 · Say hello in Discussions

⚙️ **Action required**

1. Go to the course repo and open the **Discussions** tab.
2. Find the setup thread and post the output of `python scripts/doctor.py`,
   including any failures.

**Check it worked.** Your post is visible in the thread.

**Why post it even when it passed.** It tells us the cohort is ready, it tells
you that posting works before the week you have real work to post, and the
failures are the most useful thing anyone contributes — somebody else has the
same one and has not asked yet.

## 14 · Run week 1's tests

⚙️ **Action required**

```bash
pytest tests/week_01
```

**Check it worked.** The tests run and report a result. Some may fail, and that
is fine — week 1's job is making them pass.

**Why run them before week 1.** Two reasons. It proves the whole chain works,
from clone to environment to test runner, while there is still time to fix it.
And it is your first look at the thing that decides whether your week is
finished: not your opinion, not the assistant's assurance, the tests.

---

## You are set up

Every week after this, three commands:

```bash
git pull upstream main    # collect the new material, start of each week
pytest tests/week_NN      # find out where you stand
git push                  # back up your work, end of each session
```

Then read that week's page at `docs/weeks/week-NN/README.md` and its
`spec.md`, and post your submission when you are done.

Missed a week? You are not locked out —
[`docs/program/github.md`](docs/program/github.md) has the two commands that hand
you the code you missed, and using them is not cheating.

One last thing worth saying out loud: you cannot break this course. Your fork can
be deleted and remade in thirty seconds, and you have no write access to anything
but your own copy. So when you are unsure whether a command will work, run it.
The worst case is an error message, and error messages are how all of us learned
this.
