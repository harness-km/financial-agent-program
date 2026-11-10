# Setup

Do this before week 1. There is a recorded setup session covering all of it, and
a check script that tells you exactly what is missing.

Budget an hour. If you hit fifteen minutes of trouble on any one step, stop and
switch to Codespaces — that is not giving up, it is the documented path.

## Path A — your own machine

### 1. Install the three tools

| Tool | Version | Where |
| --- | --- | --- |
| Python | 3.12 or later | [python.org/downloads](https://www.python.org/downloads/) |
| Git | any recent | [git-scm.com](https://git-scm.com/downloads) |
| VS Code | any recent | [code.visualstudio.com](https://code.visualstudio.com/) |

On Windows, tick "Add python.exe to PATH" in the installer. Nearly every
Windows setup problem on this course traces back to that checkbox.

Verify, in a new terminal:

```bash
python --version
git --version
```

If `python --version` reports 3.11 or earlier, or says the command is not found,
fix that before going further. On macOS use `python3`.

### 2. Clone and open

```bash
git clone https://github.com/harness-km/financial-agent-program.git
cd financial-agent-program
code .
```

VS Code will offer to install the recommended extensions. Accept. If you miss
the prompt, open the Extensions panel and type `@recommended`.

### 3. Create the environment

```bash
python -m venv .venv
```

Then activate it:

```bash
.venv\Scripts\activate          # Windows PowerShell
source .venv/bin/activate       # macOS / Linux
```

Your prompt should now start with `(.venv)`. Install the package:

```bash
pip install -e ".[dev]"
pre-commit install
```

In VS Code, press `Ctrl+Shift+P`, run "Python: Select Interpreter", and choose
the one inside `.venv`. Skipping this is why tests sometimes pass in the
terminal and fail in the editor.

### 4. Check it

```bash
python scripts/doctor.py
```

Every line should read PASS. Paste the whole output — including failures — into
the setup thread in Discussions.

### 5. Keys

Nothing in weeks 1 to 3 needs an API key; the cached data covers it. Before
week 4:

```bash
cp .env.example .env            # copy .env.example .env   on Windows
```

Then open `.env` and add your model key. `.env` is in `.gitignore` and must stay
there. A key committed to a public repository is live within minutes of being
pushed, and the fix is revoking it, not deleting the commit.

## Path B — Codespaces

Use this if your machine blocks installing software, or if Path A fights you.

1. Go to the repository on GitHub.
2. Click the green Code button, then the Codespaces tab, then "Create codespace
   on main".
3. Wait for the container to build, two to three minutes the first time.
4. Run `python scripts/doctor.py` in the terminal.

That is the whole setup. It is the same VS Code, the same extensions and the
same Python as Path A, because both read `.devcontainer/devcontainer.json`.

Personal GitHub accounts include a monthly allowance of Codespaces compute at no
cost — enough for this course at a few hours a week on the smallest machine.
Stop your codespace when you finish for the day (Codespaces panel, then Stop) so
it is not idling against your allowance.

Add your keys under repository Settings, then Secrets and variables, then
Codespaces — not in a file.

## Troubleshooting

**`python` not found, or the wrong version.** PATH. Reinstall with the PATH box
ticked, or use `py -3.12` on Windows and `python3` on macOS.

**`pip install -e ".[dev]"` fails with a permissions error.** The virtual
environment is not active. Look for `(.venv)` in your prompt.

**Tests pass in the terminal, fail in VS Code.** Wrong interpreter selected. See
step 3.

**`pre-commit` rejects your commit.** It is supposed to. Read what it says, fix
it, stage again. It usually reformatted your file, so `git add` and re-commit.

**Anything else.** Post the full output of `python scripts/doctor.py` plus the
exact error to the Blockers category. Full output, not a summary — the useful
detail is almost always in the line people trim.
