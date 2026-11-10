# Sprint plan

The program runs as an Agile project: eight two-week sprints across sixteen
weeks, in two releases.

This file is the plan. The live state — who has done what — lives on the GitHub
Project board, and is not mirrored here, because a mirrored board is a stale
board within two sprints.

## The cadence

Every week has one two-hour build session. Every second week adds a two-hour
consultant session, which is also the sprint boundary.

| | Week A | Week B |
| --- | --- | --- |
| Build session | 2 hrs | 2 hrs |
| Consultant session | — | 2 hrs |

Six live hours per sprint, three a week on average, plus your own build time
between sessions.

## The eight sprints

Each sprint produces two increments: something that runs, and the plan for
implementing it in a real firm. The consultant increment is always about the
artifact just built — see `docs/consultant/README.md` for the six lenses applied
to it every time.

| Sprint | Weeks | Build increment | Implementing it |
| --- | --- | --- | --- |
| 1 | 1–2 | Environment working; one raw tool call; traces you can read | *A model that can call one tool* — vendor dependency, what data leaves the firm, who holds the keys, own versus rent |
| 2 | 3–4 | Three tools and a bounded loop: an agent that answers multi-step questions | *A single multi-step agent* — where it runs, per-tool credentials, the gap between a script and something an analyst uses, how a wrong answer gets caught |
| 3 | 5–6 | Compaction, behaviour in markdown, your first skill | *Configurable behaviour* — who may edit the prompt, whether that is a production change, who watches the bill |
| 4 | 7–8 | Traces, the eval harness, a measured agent. **Release 1** | *A measured agent* — the measure a board would accept, who owns the eval set, traces as evidence and as retention liability |
| 5 | 9–10 | A working graph; query decomposition and search | *A live-web pipeline* — source policy, network egress, rate limits, and the one-agent-or-several decision with a cost attached |
| 6 | 11–12 | Grounding, relevance filtering, parallel section research | *Cited parallel research* — provenance per claim, concurrency cost, and the reviewer role that just appeared |
| 7 | 13–14 | Critic loop, approval gate, MCP bridge to your Part 1 agent | *Approvals and third-party tools* — who owns the gate, its SLA and escalation, and MCP code inside the trust boundary |
| 8 | 15–16 | Verification, decision models, container, deployment. **Release 2** | *The whole system in production* — environments, rollback, secrets, on-call, accountability, adoption |

## The board

The backlog lives on a GitHub Project attached to this repository, with three
fields beyond the defaults:

| Field | Type | What it holds |
| --- | --- | --- |
| Sprint | Iteration | Two-week iterations, 1 to 8 |
| Track | Single select | Build or Consultant |
| Week | Number | 1 to 16, for build items |

Two views: a Board filtered to the current sprint for day-to-day use, and a
Table grouped by Sprint for the whole programme.

Issues are generated from the specs, not written by hand:

```bash
python scripts/seed_issues.py --dry-run     # see what it would do
python scripts/seed_issues.py               # create and update
```

Each issue carries a marker comment naming the spec it came from, so re-running
updates the existing issue rather than creating a second one. Edit
`docs/weeks/week-NN/spec.md` and re-run; never edit the issue.

Nothing about who has done what is mirrored into this repository. The board is
the only record of state, because a second copy of a live thing is a wrong copy
within two sprints — which is also why this file holds the plan and not the
progress.

## Ceremonies

**Sprint planning** — first ten minutes of the build session that opens a
sprint. The backlog is already written; this is about what you personally intend
to get done, not estimation.

**Async standup** — a pinned thread per sprint in Discussions. Post blockers,
not status. "Still working on it" helps nobody; "my loop detection fires on the
first call and I cannot see why" gets you four answers by lunch.

**Sprint review** — first thirty minutes of the consultant session. Demos of the
build increment, which is also the material the rest of that session reasons
about. Two or three people each sprint, rotating, so everyone presents twice
across the program.

**Retrospective** — last twenty minutes of the consultant session. What to keep,
what to change, one thing to try.

**Releases** — weeks 8 and 16. The working system and the transformation plan
presented together, because they are one deliverable.

## Roles

The instructor is Product Owner and owns the backlog and the specs.

The Scrum Master role rotates: one learner per sprint, eight sprints, eight
volunteers. The role is real — run the standup thread, chase blockers, facilitate
the retro — and for a cohort of delivery professionals it is worth inhabiting
rather than watching.

Everyone else is the team.

## What we deliberately do not do

No story points. No velocity charts. No burndowns. No sprint commitment treated
as a contract.

The reason is specific rather than ideological: nobody can reliably estimate how
long an AI-assisted build task takes, including the instructor. Pointing work an
assistant will do would teach a practice that is actively wrong, and a velocity
number derived from it would be noise presented as a measurement.

What we keep is the part that does the work — a sprint goal, a visible backlog, a
published Definition of Done, a review and a retro.

## Flexibility

The sixteen weeks are a plan, not a promise. If a week lands badly or the cohort
needs longer on context engineering, the sprint boundary moves and the plan is
updated here. A plan that cannot absorb what actually happened is not an Agile
plan.
