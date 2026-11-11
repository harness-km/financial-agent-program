# Week 1 — From workflow to agent

Sprint 1. No code this week.

## What changes this week

Nothing is built. What changes is what you are looking at: by the end of the
session you can read an agent's trace and say which decisions it made at runtime
that a workflow would have made at design time.

That distinction is the whole programme in one sentence, and it is worth two
hours because almost everything people find surprising later — the cost, the
non-determinism, the fact that you cannot test it by walking the branches —
follows from it.

Your environment also has to work, which is the other half of the week and the
half that actually derails people. Run `python scripts/doctor.py` before the
session, not after.

## Why it is in this order

Week 2 writes its first line of code against a live API, and every setup problem
you have not found by then will present itself as a code problem instead. An hour
spent on the environment now is cheaper than the same hour spent in week 2 while
also trying to understand tool calling.

Reading traces first also means weeks 2 to 7 have somewhere to land. You will
build the thing whose output you have already learned to read, in the order the
trace shows it: the tool call, the loop around it, the context it carries, the
log it leaves.

## The session

A demo of the finished agent answering a question, then its trace, read line by
line. Then the same question through a fixed pipeline, and a second question the
pipeline was not shaped for, which it answers confidently and wrongly.

Then a workflow-versus-agent discussion that is mostly you talking, because this
cohort builds workflows and knows where they break better than most.

Then setup troubleshooting, live, for whoever is stuck.

No consultant session this week — it falls at the end of week 2, where it also
closes sprint 1.

## What you will have afterwards

- `python scripts/doctor.py` printing PASS on every line, pasted into the setup
  thread in Discussions
- Three traces from the demo agent, for three questions of different shapes
- Five sentences on where those three paths diverged and why, in a submission post
- No credential anywhere in your clone, and a one-sentence answer to why
  `.gitignore` is not a security control

See [`spec.md`](spec.md) for exactly what each of those has to contain.

## If you are behind

There is nothing to catch up on except the environment, and that is the one thing
you cannot skip — week 2 assumes it.

If `doctor.py` reports a failure, post the whole output to the setup thread rather
than fixing it quietly. Most failures have a known one-line answer and somebody
else has already hit yours. Fifteen minutes of trouble on any single step is the
point to switch to Codespaces, which is the documented path and not a retreat.

The five sentences can land late without blocking anything. A broken Python
install cannot.
