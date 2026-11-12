# Documentation

## Start here

| Document | What it is for |
| --- | --- |
| [../START_HERE.md](../START_HERE.md) | The setup checklist, in order. Begin here |
| [program/github.md](program/github.md) | Git and GitHub from scratch. Read this first if GitHub is new to you |
| [program/vscode.md](program/vscode.md) | VS Code from scratch, including the one setting that breaks everything |
| [program/assistant.md](program/assistant.md) | Setting up Claude, Gemini or ChatGPT, and how to work with it |
| [program/setup.md](program/setup.md) | Get your environment working. Do this before week 1 |
| [program/part-1-outline.md](program/part-1-outline.md) | Weeks 1 to 8, the single-agent model |
| [program/part-2-outline.md](program/part-2-outline.md) | Weeks 9 to 16, multi-agent systems |
| [program/sprint-plan.md](program/sprint-plan.md) | How the eight sprints map to the sixteen weeks |
| [program/definition-of-done.md](program/definition-of-done.md) | What "finished" means, every week |
| [program/ai-assistant-rules.md](program/ai-assistant-rules.md) | How to direct an assistant without losing the thread |

Security has no document of its own. Every week's spec carries a security
criterion the code has to satisfy, and it is item 2 of the Definition of Done.
The per-week criteria are listed in the two outlines.

## Each week

`weeks/week-NN/` holds two files:

- `README.md` — the week page: what changes this week, and what you will have at
  the end of it
- `spec.md` — the assignment, precise enough to prompt from, including the
  reference reading and the week's security criterion

The spec is deliberately self-contained, because `scripts/seed_issues.py` turns
it into that week's GitHub issue verbatim. Anything split into a separate file
stops being in front of the person doing the work.

Session notes, where a week produces any worth keeping, are added afterwards as
`concepts.md`. They are not promised in advance: notes that exist before the
session happened are not notes.

## The consultant track

- [consultant/README.md](consultant/README.md) — how the track works, the six
  lenses, and the eight increments
- [consultant/company-brief.md](consultant/company-brief.md) — the client
- [consultant/plan-template.md](consultant/plan-template.md) — the section
  template

Every second week asks one question about what you have just built: what would
it take for a real company to actually run this?
