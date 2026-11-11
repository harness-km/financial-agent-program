"""Week 1 — the security criterion, made executable.

Spec: docs/weeks/week-01/spec.md.

Week 1's criterion is that your clone contains no credential, and that you can say
why `.gitignore` is not a security control. The second half is a sentence you say
out loud in the session. The first half is this file.

These are the only tests in the programme that pass on a fresh clone, because week
1 builds nothing. If they fail, something is wrong with your checkout rather than
with your work — most likely a key you added before week 4 needed one.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

# Paths that must never be tracked, whatever else is in .gitignore.
MUST_BE_IGNORED = (".env", "ledger.csv", "scratchpad/", ".runs/")

# Key shapes. Each is written so that none of these patterns matches its own
# source text — a scanner that flags the scanner is a scanner nobody keeps.
#
# The leading `(?<![A-Za-z0-9])` is load-bearing and was added after a false
# positive worth knowing about: a cached NVDA headline links to a URL containing
# "risk-for-tech-companies-184212599", and without that lookbehind the pattern
# finds an OpenAI key inside the word "risk". A credential scanner that cries
# wolf on committed data gets switched off within a week, which is the real
# failure mode of security tooling.
BOUNDARY = r"(?<![A-Za-z0-9])"

CREDENTIAL_PATTERNS = {
    "OpenAI or Anthropic key": re.compile(BOUNDARY + r"sk-[A-Za-z0-9_-]{20,}"),
    "AWS access key id": re.compile(BOUNDARY + r"AKIA[0-9A-Z]{16}"),
    "GitHub token": re.compile(BOUNDARY + r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "Tavily key": re.compile(BOUNDARY + r"tvly-[A-Za-z0-9]{20,}"),
    "LangSmith key": re.compile(BOUNDARY + r"lsv2_[a-z]{2}_[A-Za-z0-9]{32,}"),
    "PEM private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}

MAX_SCAN_BYTES = 2_000_000


def tracked_files() -> list[Path]:
    """Every file git is tracking, which is every file you could have pushed."""
    if shutil.which("git") is None:
        pytest.skip("git is not on PATH — run scripts/doctor.py")
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:  # pragma: no cover
        pytest.skip(f"git would not run: {exc}")
    if out.returncode != 0:
        pytest.skip("not a git checkout — these tests check what git is tracking")
    return [ROOT / name for name in out.stdout.split("\0") if name]


# --- what git is tracking -------------------------------------------------------


def test_repository_is_a_git_checkout() -> None:
    """The rest of this file is about git's index, so there has to be one."""
    assert tracked_files(), "git is tracking no files"


def test_env_is_not_tracked() -> None:
    """The one file that must never be committed."""
    names = {path.name for path in tracked_files()}
    assert ".env" not in names


def test_env_example_is_tracked() -> None:
    """The template is meant to be in the repository. Only the filled-in copy is not."""
    names = {path.name for path in tracked_files()}
    assert ".env.example" in names


def test_no_env_file_anywhere_is_tracked() -> None:
    """`.env.local`, `.env.production` and friends are covered by .gitignore too."""
    tracked = [
        path.relative_to(ROOT).as_posix()
        for path in tracked_files()
        if path.name.startswith(".env") and path.name != ".env.example"
    ]
    assert tracked == []


# --- what .gitignore covers -----------------------------------------------------


@pytest.mark.parametrize("pattern", MUST_BE_IGNORED)
def test_gitignore_covers(pattern: str) -> None:
    """`.env` from week 1, `ledger.csv` from week 2, `scratchpad/` from week 7.

    Each one is a file your own work creates. The ignore has to exist before the
    week that creates it, not after.
    """
    lines = {
        line.strip() for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    }
    assert pattern in lines, f"{pattern} is not in .gitignore"


def test_gitignore_is_not_a_security_control() -> None:
    """The week's actual lesson, written down where it cannot be skipped.

    `.gitignore` stops an accident, not a decision. It does nothing about a key
    pasted into a notebook cell, a prompt or a trace file — which is why the
    credential scan below reads every tracked file rather than trusting the
    ignore list. If `.gitignore` were the control, that scan would be redundant.
    """
    ignored = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in ignored
    assert tracked_files(), "and yet the scan still has to look"


# --- the credential scan --------------------------------------------------------


def test_no_credential_in_any_tracked_file() -> None:
    """Every file git is tracking, read, and checked against six key shapes.

    This is the week 1 criterion. In week 7 you will grep your own trace files
    for the same thing and expect the same answer.
    """
    findings: list[str] = []
    for path in tracked_files():
        if not path.is_file() or path.stat().st_size > MAX_SCAN_BYTES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in CREDENTIAL_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{path.relative_to(ROOT).as_posix()}: {label}")
    assert findings == [], "credential-shaped strings found: " + "; ".join(findings)


def test_env_example_holds_no_key_values() -> None:
    """The template names the variables and sets none of them.

    `FIN_AGENT_MODEL=gpt-5.4-mini` is fine — a model name is not a secret. Any
    variable whose name ends in `_API_KEY` has to be empty.
    """
    filled: list[str] = []
    for line in (ROOT / ".env.example").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        if name.strip().endswith("_API_KEY") and value.strip():
            filled.append(name.strip())
    assert filled == [], f"{', '.join(filled)} has a value in .env.example"
