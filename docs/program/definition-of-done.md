# Definition of Done

Nothing on this course is graded. This list replaces grading.

It is identical every week, published in advance, and every item is something
you can check yourself. Your work is visible to the cohort rather than marked by
the instructor, which is a higher bar rather than a lower one.

An increment is done when all six hold.

## 1. The week's tests pass

```bash
pytest tests/week_NN
```

The tests are the spec made executable. They assert against cached data, so the
expected values are exact and there is no judgement call about whether you are
finished.

If a test is wrong — and some will be — say so in Blockers. A test nobody
challenges for sixteen weeks is more likely stale than correct.

## 2. The week's security requirement is met

Every spec carries one, stated as an acceptance criterion rather than a topic.
Week 3's tools reject tickers outside the list. Week 4's loop cannot run
unbounded. Week 7's traces do not contain your key.

There is no security module on this course and no session where we "do"
security, because that is not where it lives in real work. It is in the spec
because that is where it has to be: you do not add it afterwards, and the
assistant writing your code will not add it unprompted.

From week 4 most of these criteria land in the same place: the pre-tool and
post-tool hook pair you build around tool dispatch. Each week adds a policy to
it rather than a mechanism of its own, so by week 16 one seam holds the result
caps, the injection handling, the redacted audit trail, the domain allowlist,
the credential scoping and the publication gate.

The wording of this item never changes. What it requires is set by the week.

## 3. Your eval score is recorded

From week 7, when the eval harness exists. Run it, record the number, and put it
in your submission post.

A lower score than last week is information, not failure. The interesting
submissions are the ones that explain why a change made the score worse.

## 4. Your cost ledger row is committed

Model, calls, tokens in, tokens out, cost for the run. From week 2, when the
ledger exists.

This is here because an agent's cost is a design property, not an accounting
detail. By week 5 you will be reading your own ledger to tell whether compaction
worked.

## 5. Your prompt trail is posted

The prompts you used, in order, including the ones that went wrong. The failed
prompts are the useful ones.

This is the item that carries the most weight. You cannot write a good spec for
a component you do not understand, so the trail shows your grasp of the
architecture more directly than the code does. Two people with identical working
code have not necessarily learned the same thing, and the trail is where the
difference shows.

## 6. Your consultant-track section is added

One section of the transformation plan for the client in
`docs/consultant/company-brief.md`, following `docs/consultant/plan-template.md`.
Due at the sprint boundary, so every second week.

Its risk and governance lens is where the week's security work surfaces as a
client-facing argument — the same concern, one level up.

The code half and the organisation half of this program are the same
deliverable. A system nobody can implement in a real firm is a demo.

## What is deliberately not on this list

Elegant code. Complete coverage. Matching the reference implementation. Finishing
first.

If your version passes its tests, meets its security criterion, and you can
explain every line and what it cost to run, it is done — whatever it looks like
next to someone else's.
