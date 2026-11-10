# Financial Agent Program

Build a financial analyst agent, then turn it into a multi-agent research system.

This repository is the working environment for the program. It holds the weekly
specs, the starter code, the cached market data, the tests your work has to pass,
and the sprint backlog that tracks it all.

It is also the first worked example you will see. The templates, the linting, the
CI workflow and the commit conventions in here are the practices the course
teaches, applied to the course itself.

## Quick start

1. Install [VS Code](https://code.visualstudio.com/), [Git](https://git-scm.com/)
   and Python 3.12.
2. Clone this repository and open the folder in VS Code. Accept the prompt to
   install the recommended extensions.
3. Create and activate a virtual environment, then install the package:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS / Linux
   pip install -e ".[dev]"
   ```

4. Run the environment check and post its output to the setup discussion:

   ```bash
   python scripts/doctor.py
   ```

If installing locally is blocked on your machine, open this repository in
**GitHub Codespaces** instead. It is the same VS Code and the same container, in
a browser tab, and it needs nothing installed. See `docs/program/setup.md`.

## Where things are

| Path | What is in it |
| --- | --- |
| `docs/program/` | Outlines, sprint plan, Definition of Done, ground rules |
| `docs/weeks/week-NN/` | The week page, its spec, concepts and reference reading |
| `docs/consultant/` | The fictional company brief and the transformation plan template |
| `starters/week-NN/` | The starting point for that week's assignment |
| `src/fin_agent/` | The package you build. All logic lives here, not in notebooks |
| `cache/` | Pre-fetched market data for ten tickers. Deterministic by design |
| `tests/` | The tests each week's spec is checked against |
| `evals/` | Eval question sets |
| `scripts/` | `doctor.py` and repository tooling |

## How a week works

1. Read `docs/weeks/week-NN/README.md` and its `spec.md`.
2. Build it, directing your AI assistant with the rules in
   `docs/program/ai-assistant-rules.md`.
3. Run the week's tests: `pytest tests/week_NN`.
4. Open a pull request and post your submission, meeting every item in
   `docs/program/definition-of-done.md`.

Missed a week? Every week has a known-good starting point. Check out
`week-NN-start` and carry on — you are never locked out of the next session.

## Disclaimer

This program is educational. The agent analyses public financial data and
produces structured opinions. Nothing it produces is investment advice, and
nothing here should be acted on as such.
