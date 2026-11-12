#!/usr/bin/env python3
"""Create or update the backlog on GitHub from the specs in this repository.

The specs are the source of truth. This script pushes them to GitHub issues, so
you edit `docs/weeks/week-NN/spec.md` and re-run this — never the issue.

It reads:
    docs/weeks/week-NN/spec.md              kind: build
    docs/consultant/sprint-NN/increment.md  kind: consultant

Each file has a small frontmatter block followed by the spec itself. The body is
passed through verbatim as the issue body, with a marker comment appended so
re-runs update the existing issue instead of creating a second one.

Usage:
    python scripts/seed_issues.py --dry-run          # show what would happen
    python scripts/seed_issues.py                    # create and update
    python scripts/seed_issues.py --only week-04     # one spec

Requires the `gh` CLI, authenticated (`gh auth login`). Standard library only,
on purpose: this has to run in a bare checkout.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "<!-- seeded-from: {source} -->"
MARKER_RE = re.compile(r"<!-- seeded-from: (?P<source>[^ ]+) -->")

REQUIRED = ("kind", "week", "sprint", "title")
VALID_KINDS = ("build", "consultant")


@dataclass
class Spec:
    source: str
    kind: str
    week: str
    sprint: str
    title: str
    body: str

    @property
    def issue_title(self) -> str:
        if self.kind == "build":
            return f"Week {self.week} — {self.title}"
        return f"Sprint {self.sprint} — implementing {self.title}"

    @property
    def labels(self) -> list[str]:
        return [self.kind, f"sprint-{self.sprint}"]

    @property
    def issue_body(self) -> str:
        return f"{self.body.rstrip()}\n\n{MARKER.format(source=self.source)}\n"


def parse_frontmatter(text: str, source: str) -> tuple[dict[str, str], str]:
    """Split `--- key: value --- body`.

    A deliberately small subset of YAML: one `key: value` per line, no nesting,
    no lists. Anything more belongs in the body.
    """
    if not text.startswith("---"):
        raise ValueError(f"{source}: missing frontmatter block")
    try:
        _, front, body = text.split("---", 2)
    except ValueError as exc:
        raise ValueError(f"{source}: frontmatter block is not closed") from exc

    meta: dict[str, str] = {}
    for line in front.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{source}: cannot parse frontmatter line: {line!r}")
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip("\"'")

    missing = [k for k in REQUIRED if k not in meta]
    if missing:
        raise ValueError(f"{source}: frontmatter missing {', '.join(missing)}")
    if meta["kind"] not in VALID_KINDS:
        raise ValueError(f"{source}: kind must be one of {VALID_KINDS}")

    return meta, body.lstrip("\n")


def load_specs(only: str | None) -> list[Spec]:
    paths = sorted(ROOT.glob("docs/weeks/week-*/spec.md")) + sorted(
        ROOT.glob("docs/consultant/sprint-*/increment.md")
    )
    specs: list[Spec] = []
    for path in paths:
        source = path.relative_to(ROOT).as_posix()
        if only and only not in source:
            continue
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"), source)
        specs.append(
            Spec(
                source=source,
                kind=meta["kind"],
                week=meta["week"],
                sprint=meta["sprint"],
                title=meta["title"],
                body=body,
            )
        )
    return specs


def gh(*args: str) -> str:
    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=False, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result.stdout


def existing_issues() -> dict[str, int]:
    """Map each spec path to the issue number already seeded from it."""
    raw = gh(
        "issue",
        "list",
        "--state",
        "all",
        "--limit",
        "200",
        "--json",
        "number,body",
    )
    found: dict[str, int] = {}
    for issue in json.loads(raw or "[]"):
        match = MARKER_RE.search(issue.get("body") or "")
        if match:
            found[match.group("source")] = issue["number"]
    return found


def label_style(name: str) -> tuple[str, str]:
    """Colour and description for a label this script is about to create."""
    if name == "build":
        return "1d76db", "A week's build increment, generated from its spec"
    if name == "consultant":
        return "5319e7", "A sprint's consultant increment, generated from its spec"
    if name.startswith("sprint-"):
        return "0e8a16", f"Sprint {name.removeprefix('sprint-')}"
    return "ededed", "Generated by scripts/seed_issues.py"


def ensure_labels(labels: set[str]) -> None:
    """Create any label the specs ask for that the repository does not have.

    `gh issue create --label` fails outright on a label that does not exist, so
    on a fresh repository every issue fails before this ran. The labels come from
    the specs' own frontmatter — `build`, `consultant`, `sprint-1` through
    `sprint-8` — which makes them this script's business rather than something to
    create by hand and then recreate on the next fork of the repository.
    """
    raw = gh("label", "list", "--limit", "200", "--json", "name")
    existing = {label["name"] for label in json.loads(raw or "[]")}
    for name in sorted(labels - existing):
        colour, description = label_style(name)
        gh("label", "create", name, "--color", colour, "--description", description)
        print(f"  label        {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="print, change nothing")
    parser.add_argument("--only", help="substring of the spec path, e.g. week-04")
    args = parser.parse_args()

    try:
        specs = load_specs(args.only)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not specs:
        print("No specs found. Expected docs/weeks/week-NN/spec.md")
        return 0

    if args.dry_run:
        for spec in specs:
            print(f"  {spec.source:44} -> {spec.issue_title}  {spec.labels}")
        print(f"\n{len(specs)} spec(s). Re-run without --dry-run to apply.")
        return 0

    try:
        ensure_labels({label for spec in specs for label in spec.labels})
        seeded = existing_issues()
    except (RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        print("Is the `gh` CLI installed and authenticated? Try: gh auth status")
        return 1

    created = updated = failed = 0
    for spec in specs:
        body_file = ROOT / ".seed-body.tmp"
        body_file.write_text(spec.issue_body, encoding="utf-8")
        try:
            number = seeded.get(spec.source)
            if number:
                gh(
                    "issue",
                    "edit",
                    str(number),
                    "--title",
                    spec.issue_title,
                    "--body-file",
                    str(body_file),
                )
                print(f"  updated #{number}  {spec.issue_title}")
                updated += 1
            else:
                out = gh(
                    "issue",
                    "create",
                    "--title",
                    spec.issue_title,
                    "--body-file",
                    str(body_file),
                    *sum((["--label", label] for label in spec.labels), []),
                )
                print(f"  created      {spec.issue_title}  {out.strip().splitlines()[-1]}")
                created += 1
        except RuntimeError as exc:
            print(f"  FAILED       {spec.source}: {exc}", file=sys.stderr)
            failed += 1
        finally:
            body_file.unlink(missing_ok=True)

    print(f"\n{created} created, {updated} updated, {failed} failed.")
    if failed:
        # Exiting 0 on a seeding run that created nothing is how a backlog ends
        # up half-populated without anybody noticing.
        print("Nothing above is retried automatically. Fix and re-run.", file=sys.stderr)
        return 1

    print("Assign them to their Sprint iteration on the project board.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
