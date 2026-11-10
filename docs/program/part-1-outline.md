# Part 1 — Fundamentals and the single-agent model

Weeks 1 to 8, sprints 1 to 4.

By week 8 you have a working financial analyst agent: it plans its own research,
calls tools, manages its own context, loads behaviour from editable files, and is
scored against a test set. You will have built it by specifying it, week by week.

The reference project for Part 1 is [Dexter](https://github.com/virattt/dexter),
an autonomous financial research agent. It is TypeScript, so we read it rather
than run it, and rebuild the architecture in Python. We are after its methods —
the loop, the caps, the context handling, the scratchpad — not its line count.

## Security is an acceptance criterion, not a topic

There is no security session. Every week's spec carries a security requirement
that the code has to satisfy, and it is item 2 of the Definition of Done.

This is deliberate. Security taught as its own module gets learned as its own
module and then left out of everything else — which is exactly what happens in
practice when it is somebody else's section of the document.

From week 4 the criteria mostly land in one place. You build a pre-tool and
post-tool hook pair around tool dispatch, and every week after that adds a
policy to it: result caps in week 5, injection handling in week 6, redacted
logging in week 7, an allowlist in week 10, credential scoping in week 12. One
chokepoint, nine weeks of policy. If you have worked with middleware or
interceptors, this is that pattern, and the reason is the same — policy belongs
at the boundary, not scattered through the logic.

## At a glance

| Week | Focus | What you build | Security criterion |
| --- | --- | --- | --- |
| 1 | From workflow to agent | Environment only | No credential anywhere in your clone |
| 2 | What an LLM does, and how to direct one | One raw tool call | Model output parsed and validated before use |
| 3 | Tools are the product | Three tools over cached data | Each tool rejects inputs outside the allowed set |
| 4 | The agent loop | The loop, caps, and the hook pair | Every tool call passes through hooks that can deny it |
| 5 | Context engineering | Compaction and a result size cap | Post-tool hook caps results; offloaded context gitignored and credential-free |
| 6 | Behaviour as configuration | Prompt in markdown, plus one skill | Post-tool hook marks fetched text as data; one injection attempt demonstrably fails |
| 7 | Observability and evaluation | Trace logging and the eval harness | Hooks log every call and outcome, redacted — no key, no client identifier |
| 8 | Capstone | Nothing new — consolidation | The hook policy and the seven criteria argued as one posture |

## Week 1 — From workflow to agent

A deterministic workflow versus a path the model chooses at runtime, and what
that breaks: you can no longer read the flow off a canvas, test by walking the
branches, or predict the cost.

Demo: the finished agent answering a question, then its trace. Then a fixed
pipeline doing the same task and failing on a question it was not shaped for.

Assignment: no coding. Run the reference agent on three questions of your own,
read all three traces, write five sentences on where the paths diverged and why.

Done when: your clone contains no credentials, `git status` shows no `.env`, and
you can say why `.gitignore` is not itself a security control — it stops an
accident, not a decision.

## Week 2 — What an LLM does, and how to direct one

First hour: tokens, context window, temperature, and the central deflation — the
model never calls a tool. It emits structured JSON and your code decides whether
to honour it. Nothing about the model is agentic; the agency is in the loop.

That deflation is also the week's security point, and they are the same
sentence. If your code is what decides, then your code is the control, and
whatever the model emitted is input from an untrusted source — because it is
downstream of whatever the model has read. The hooks you build in week 4 are
where that decision gets a name and a place to live.

Second hour: directing an assistant. We watch a vague prompt produce a hundred
lines of invented abstractions, then a spec-based prompt produce the thing. The
seven rules in `ai-assistant-rules.md` start here.

Build: one tool call by hand against the raw API, no framework, about fifteen
lines. Plus the cost ledger, which instruments everything from here on.

Reading: how Dexter's tool executor sits between the model and the tool.

Done when: your code parses and validates the model's arguments before acting on
them, and fails closed on anything it does not recognise.

## Week 3 — Tools are the product

Tool naming, the docstring as prompt surface, parameter schemas, and return
formatting. Dexter returns formatted text rather than raw JSON for token
economy, which is worth ten minutes on its own.

Demo: build a tool live against the cache, then give it a vague description and
watch the model misuse it. The misuse is the lesson — and the misuse is also the
attack, because a tool with a loose contract is a tool that will be called in
ways you did not plan for.

Build: three tools — income statement, prices, news — each with a proper schema
and docstring, each passing the provided tests.

Reading: `src/tools/finance/` — one tool file plus `formatters.ts`.

Done when: every tool validates its own inputs and rejects any ticker outside
`config.TICKERS`. The hook in week 4 will check the same things centrally, and
both layers stay — a tool that is only safe because something upstream protects
it is not a safe tool.

## Week 4 — The agent loop and the hook pair

The while loop, the iteration cap, repeated-call detection, read-only versus
state-changing tools and why only the former are safe to run concurrently, and
abort handling.

Then the piece that carries the rest of the programme. Instead of the loop
calling tools directly, every call goes through two functions:

```python
def before_tool(name: str, args: dict) -> dict:   # may rewrite args, or raise Deny
def after_tool(name: str, result: str) -> str:    # may rewrite or truncate the result
```

Both are thin this week — they log the call, enforce the caps and check the
budget. That is the point. You build the seam now, while it is fifteen lines and
obvious, and every later week has somewhere to put its policy. A control added
at a boundary that already exists is a small change; the same control retrofitted
into nine call sites is the reason security work gets deferred indefinitely.

Demo: build the loop live, around forty lines, then the hooks. Then remove the
cap and let it thrash on an ambiguous question with the token counter on screen —
an unbounded loop is a cost incident, the pre-tool hook is where the budget check
lives, and the ledger is how anyone would notice.

Build: the loop with cap and repeated-call detection, the hook pair, your three
tools bound through it.

Reading: `src/agent/agent.ts` for the loop, then `src/agent/tool-executor.ts` —
that file is this week's design, with approval gating, concurrency and abort
already in it.

Done when: no tool can be invoked except through the hooks, a denied call raises
rather than returning something the model might believe, and you can show the
ledger row from the uncapped run you did on purpose.

## Week 5 — Context engineering

The week with no workflow-tool analogue, and the one that separates a demo from a
system. Why token growth degrades long sessions, compaction versus per-turn
microcompaction, tool-result size caps, offloading large results to disk.

The size cap goes in the post-tool hook, which is the first policy your seam
carries. A tool that returns a megabyte is a context problem and a cost problem
at once, and the hook handles both in one place regardless of which tool did it.

Demo: the token curve across a ten-iteration run, then the same run with
compaction. The two curves side by side do the teaching.

Offloading is also the first time your agent writes data somewhere, which makes
retention a design decision you are now making whether or not you notice.

Build: a compaction pass, and a per-result size cap in the post-tool hook.
Deliverable is the before-and-after token plot, so success is visible without
judging code.

Reading: `compact.ts` and `microcompact.ts`.

Done when: the post-tool hook enforces the cap for every tool, everything written
to disk goes to a gitignored path, you can state its retention in one sentence,
and nothing written there contains a credential.

## Week 6 — Behaviour as configuration

System prompt assembly, the injected-markdown-document pattern, and skills as
folders of procedure rather than code. The point that matters most here: once
behaviour lives in markdown, you change what the agent does without touching
Python.

Which is the whole week in one sentence, both ways round. A file that changes
behaviour without changing code is a powerful thing to hand a non-engineer, and
it is also an injection surface — as is every page, note and document the agent
reads.

The post-tool hook is the defence, and it is a structural one rather than a
filter: whatever comes back from a tool gets wrapped and labelled as data before
it reaches the model's context. You are not trying to recognise malicious text.
You are making the boundary between instruction and content explicit, so there is
nothing for injected text to be mistaken for.

Demo: externalise the rules, edit them live, rerun, different behaviour, zero
code change. Then add a DCF skill. Then plant an instruction in a document the
agent reads and watch it fail to take effect.

Build: externalise your prompt, write one skill in a domain you care about, and
add content wrapping to the post-tool hook.

Reading: `prompts.ts`, `SOUL.md`, `src/skills/dcf/`.

Done when: fetched and injected text is structurally marked as data, and you can
demonstrate one injection attempt that fails.

## Week 7 — Observability and evaluation

The JSONL scratchpad you have been reading since week 1, now built properly —
and it comes almost free, because the hooks already see every call. The pre-tool
hook logs intent, the post-tool hook logs outcome, and redaction happens in one
place rather than at every log statement.

Then tracing, LLM-as-judge, and what accuracy means for an agent whose path
varies between runs.

Then the half of evaluation that usually goes missing: not scoring, but fixing.
Low completeness usually means tool coverage or the iteration cap. Low relevance
usually means context pollution or a vague tool description. Wrong numbers mean
the tool, not the model. Degradation late in a run means compaction. Everything
from weeks 2 to 6 is the repair kit.

A trace is the most complete record of everything your agent touched, which makes
it both your best debugging instrument and the most sensitive file in the
repository.

Build: scratchpad logging in the hooks with redaction, then run the ten-question
eval and submit the score plus one failure diagnosed from its trace.

Reading: `scratchpad.ts` and `src/evals/`.

Done when: every tool call and its outcome is logged through the hooks, and you
have grepped your own trace files for your key and for anything
client-identifying and found nothing.

## Week 8 — Capstone and Release 1

No new architecture. Student demos, then an honest accounting of the gap between
what you built and the real thing: what Dexter's extra couple of thousand lines
buy, and what they do not.

The seven criteria are now one thing — a policy layer you can point at, with
four behaviours attached to it — rather than a checklist. That is the posture
presented at Release 1, and for this audience it is the most portable thing in
Part 1: a defensible position on agent security arrived at by building one.

Closes by setting up Part 2 — where a single loop genuinely fails, and why that
is a different course rather than more of this one.
