#!/usr/bin/env python3
"""Check this machine can run the course. Standard library only, on purpose:
this has to work before anything is installed.

Usage:
    python scripts/doctor.py
    python scripts/doctor.py --no-keys    # skip API key checks (used by CI)
"""

from __future__ import annotations

import importlib.util
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_PYTHON = (3, 12)
REQUIRED_IMPORTS = ["langchain", "pydantic", "yfinance", "pytest"]
EXPECTED_TICKERS = 10

results: list[tuple[bool, str, str]] = []


def check(ok: bool, label: str, detail: str = "") -> None:
    results.append((ok, label, detail))


def check_python() -> None:
    v = sys.version_info
    ok = (v.major, v.minor) >= MIN_PYTHON
    check(
        ok,
        "Python version",
        f"{v.major}.{v.minor}.{v.micro}"
        + ("" if ok else f" — need {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or later"),
    )


def check_venv() -> None:
    active = sys.prefix != sys.base_prefix
    check(
        active,
        "Virtual environment",
        "active" if active else "not active — run the venv step in the README",
    )


def check_git() -> None:
    path = shutil.which("git")
    if not path:
        check(False, "Git", "not found on PATH")
        return
    try:
        out = subprocess.run(
            ["git", "--version"], capture_output=True, text=True, timeout=10
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError) as exc:
        check(False, "Git", f"found but would not run: {exc}")
        return
    check(True, "Git", out)


def check_imports() -> None:
    missing = [m for m in REQUIRED_IMPORTS if importlib.util.find_spec(m) is None]
    check(
        not missing,
        "Dependencies",
        "all present"
        if not missing
        else f"missing {', '.join(missing)} — run: pip install -e \".[dev]\"",
    )


def check_package() -> None:
    ok = importlib.util.find_spec("fin_agent") is not None
    check(
        ok,
        "fin_agent importable",
        "yes" if ok else 'no — run: pip install -e ".[dev]"',
    )


def check_cache() -> None:
    cache = ROOT / "cache"
    if not cache.is_dir():
        check(False, "Cached market data", "cache/ folder is missing")
        return
    tickers = sorted(p.name for p in cache.iterdir() if p.is_dir())
    ok = len(tickers) >= EXPECTED_TICKERS
    check(
        ok,
        "Cached market data",
        f"{len(tickers)} tickers: {', '.join(tickers) or 'none'}"
        + ("" if ok else f" — expected {EXPECTED_TICKERS}"),
    )


def check_keys() -> None:
    key = os.environ.get("OPENAI_API_KEY", "")
    dotenv = (ROOT / ".env").is_file()
    if key:
        check(True, "Model API key", f"set, ends {key[-4:]}")
    elif dotenv:
        check(True, "Model API key", ".env present (not loaded by this script)")
    else:
        check(
            True,
            "Model API key",
            "not set — fine until week 4, then copy .env.example to .env",
        )


def main() -> int:
    skip_keys = "--no-keys" in sys.argv

    print("\nFinancial Agent Program — environment check")
    print(f"{platform.system()} {platform.release()}  ·  {ROOT}\n")

    check_python()
    check_venv()
    check_git()
    check_imports()
    check_package()
    check_cache()
    if not skip_keys:
        check_keys()

    width = max(len(label) for _, label, _ in results)
    failed = 0
    for ok, label, detail in results:
        mark = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        print(f"  [{mark}]  {label.ljust(width)}   {detail}")

    print()
    if failed:
        print(f"{failed} check(s) failed. Paste this whole output into the setup thread.")
        print("Fifteen minutes of trouble is the point to switch to Codespaces.\n")
        return 1

    print("All checks passed. Post this output to the setup thread.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
