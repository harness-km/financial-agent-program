# Part 2 — Multi-agent research and decision systems

Weeks 9 to 16, sprints 5 to 8. Part 1 is the prerequisite.

By week 16 you have a system that plans an outline, researches sections in
parallel, reviews its own work, reaches external tools over the Model Context
Protocol, ends in a structured decision you can check for hallucination, and
runs in a container at a public URL.

The reference project is
[GPT Researcher](https://github.com/assafelovic/gpt-researcher). It is Python, so
we can run it as well as read it. It is three stacked layers — a single-agent
research engine, a LangGraph multi-agent team, and a Deep Agents harness — and
that stack maps almost exactly onto this half of the program.

## Security is an acceptance criterion, not a topic

Same as Part 1: no security session, a requirement in every spec, item 2 of the
Definition of Done.

The hook pair from week 4 carries most of it. Every tool call in the graph —
including the ones that reach out to the open web and the ones that go through
MCP to somebody else's server — traverses the same two functions, so each week's
policy is one addition in one place rather than a change to every node. By week
16 that seam holds the allowlist, the credential scoping, the rate limits, the
audit record and the publication gate.

That is the argument for building it in week 4 rather than week 14. A graph has
more places to go wrong than a loop, and a system where every node implements its
own controls is a system where they are implemented differently.

## At a glance

| Week | Focus | What you build | Security criterion |
| --- | --- | --- | --- |
| 9 | When one loop is not enough | A three-node graph | State validated at every node boundary |
| 10 | Research as a pipeline | Query decomposition and search | Pre-tool hook enforces a domain allowlist; private addresses refused |
| 11 | Grounding beats cleverness | Fetching, filtering, a cited report | Every claim carries a resolvable source |
| 12 | The graph | Planner plus parallel researchers | Pre-tool hook enforces per-node credential scope and rate limits |
| 13 | Critics, bounds and the human gate | Fact-checker with a cap, approval gate | Hooks record every verdict and approval; a skipped gate is visible |
| 14 | The Model Context Protocol | Your Part 1 agent as a tool | MCP calls traverse the same hooks; out-of-scope requests refused |
| 15 | Verification and decision models | Two-tier verification, structured decisions | Publication blocked without a retained verification record |
| 16 | Capstone | Container and deployment | No secret in the image; nothing unintended exposed |

## Week 9 — When one loop is not enough

Honest cost and benefit. Where single agents genuinely fail: work with
independent parallel parts, objectives that conflict and need separating, output
longer than one context window handles well, steps needing different
permissions. And where multi-agent is expensive theatre.

The decision framing: this is the same call as splitting a monolith into
services. You already know what coordination overhead costs. Every agent you add
multiplies the places state can go wrong, and most published multi-agent systems
would run better as one well-bounded loop. Being able to argue that out loud is
worth more than the LangGraph syntax.

That is also why the week's criterion is about boundaries. In a loop there is one
place state lives; in a graph there are as many as you have nodes, and a node
that accepts whatever it is handed will pass a problem along silently. Your tool
calls already go through a validated seam. Your node edges do not yet.

Build: a three-node graph that passes state, with the tool hooks carried over
intact.

Assignment: take your Part 1 agent, name one task it does badly, and argue in
half a page whether a graph would actually fix it.

Done when: every node validates its inputs at the boundary and fails loudly
rather than forwarding malformed state.

## Week 10 — Research as a pipeline

Query decomposition and the retriever abstraction. One question becomes several
sub-queries; a retriever interface means a new source changes no other code.

This is also the week your system starts fetching things people you have never
met control. A page is input, and a filter that tries to recognise bad input will
always lose to an allowlist that defines good input. Both go in the pre-tool
hook — which already exists, so this week's security work is one policy addition
rather than a new mechanism.

Reading: `actions/query_processing.py`, the best file in the repository for this,
at roughly two hundred lines.

Build: query decomposition and a web search tool. This is where you leave the
cache, and where your results stop matching everyone else's.

Done when: the pre-tool hook restricts fetching to an allowlist, refuses requests
to private address ranges, and you can demonstrate a blocked fetch.

## Week 11 — Grounding beats cleverness

Page fetching, relevance filtering with embeddings and a similarity threshold,
and cited writing.

The aha: filtering quality beats agent sophistication. This is the real
anti-hallucination layer, and it sits upstream of any fact-checker.

It is also where provenance becomes real. A claim you cannot trace is a claim the
firm cannot defend, months later, to someone who doubts it — which makes citation
an audit requirement rather than a courtesy. The post-tool hook is a natural
place to attach source metadata to everything that enters context, so that
tracing a claim later is a lookup rather than an investigation.

Reading: `skills/context_manager.py` and `curator.py`.

Build: a cited mini-report. Produce it with and without the relevance filter and
explain the difference.

Done when: every claim in the output resolves to a source that was actually
fetched, and an unsourced claim fails your own test.

## Week 12 — The graph

`StateGraph`, a typed state object, and fan-out: one researcher subgraph per
outline section, running in parallel. Watch state-merge conflicts; this is where
most first multi-agent builds break.

Fan-out multiplies what any single node could do with what it holds, which is the
argument for not handing every node the same credentials. It is also the point at
which rate limits stop being a performance concern and become a way to get your
account suspended. Both are pre-tool hook policies, keyed on which node is
calling — the first time your hook needs to know who is asking, not just what
for.

Reading: `multi_agents/agents/orchestrator.py` — `_add_workflow_edges` is the
whole architecture in fifteen lines.

Build: a graph that researches three sections at once and merges them without
losing state.

Done when: the pre-tool hook grants each node only the credentials its own work
requires, and your concurrency respects the published rate limits of everything
it calls.

## Week 13 — Critics, bounds and the human gate

A fact-checker node, a conditional edge back to the writer, and a hard revision
cap. We run a critic loop uncapped once, deliberately, and watch it thrash.

Then the human gate: an approval node after the planner, with interrupt, resume
and checkpointing. Approval nodes are familiar from workflow tools; what is new
is resuming when a model was mid-reasoning.

A critic is a control, and so is an approval step. Controls that leave no record
are not controls — nobody can show afterwards that the gate was passed rather
than skipped, which is the first thing anyone will ask. Your hooks already write
an audit trail for tool calls; this week they start writing one for decisions.

Build: a critic that rejects a draft once, a cap that provably stops it looping,
and an approval gate you can pause at and resume from without rerunning the
research.

Done when: every critic verdict and every human approval is recorded with who,
what and when, and a skipped gate is visible in the record.

## Week 14 — The Model Context Protocol

Protocol basics, servers versus clients, transports. The architectural insight
worth the session: GPT Researcher exposes MCP as a *retriever*, so any server
becomes a research source without touching the graph. Tool selection is itself an
LLM call, with a pattern-matching fallback.

A server is code you did not write, running inside your trust boundary, holding
scopes you granted it. That is the whole week's security question and it is not
hypothetical — it is what any firm's vendor assessment will ask you.

The answer is the seam again, from both directions. Calls out to a third-party
server go through your pre-tool hook, so a vendor's tool inherits your allowlist,
your budget check and your audit trail whether or not the vendor implemented any
of them. And your own server, the one exposing your Part 1 agent, declares and
enforces its scopes — because somebody else is about to treat you as the
third party.

Reading: `gpt_researcher/mcp/tool_selector.py`, then `client.py`.

Build: expose your Part 1 agent as an MCP server and consume it as a research
source in your graph, changing no graph code.

This is the hinge of both courses. The agent you spent eight weeks building
becomes a component in something larger, which is the actual shape of production
systems.

Done when: MCP calls traverse the same hooks as every other tool, your server
declares its scopes and allowed root paths, and a request outside them is
refused.

## Week 15 — Verification and decision models

Two-tier verification: numeric claims checked deterministically against the
structured source, narrative claims checked by an LLM judge. Financial
hallucination is mostly numeric, so a judge alone is the wrong tool for the
dangerous errors.

Then decision models: convert the narrative into a typed object with thesis,
conditions, sizing, confidence and explicit falsifiers, and gate publication on
the verification result.

At which point verification stops being a quality measure and becomes
governance. Someone is accountable for a decision this system produced, and what
they will need is the record of why it was published. Publication is a tool call
like any other, so the gate is a post-tool hook — which means it cannot be
bypassed by a node that forgot to check.

Reading: `evals/hallucination_eval/evaluate.py`.

Build: a decision object with conditions and falsifiers, published only if
verification passes.

Done when: publication is impossible without a passed verification, and the
verification record is retained alongside the decision it cleared.

## Week 16 — Capstone and Release 2

The contrast case first: `deep_agents/` achieves the same plan-research-review
behaviour with the graph deleted — planning becomes a todo tool, fan-out becomes
subagent spawning, state becomes a filesystem. Their README has the comparison
table. This lands only because you hand-wired the graph in weeks 12 and 13.

It is worth noticing what survives that deletion. The hook pair does, because it
sits around tool dispatch rather than inside the orchestration — which is a
reasonable definition of a good architectural seam, and a point worth making out
loud at Release 2.

Then containerisation and deployment. Your development environment has been a
container since the setup session, so this is a smaller step than it sounds. The
host is chosen in the week we need it, not in advance: free tiers in this market
change every few months, and refusing to lock a dependency four months early is
itself the lesson.

Build: a container for your system and a deployed public instance.

Assignment: re-point the system at a question in your own field, deploy it, and
present it — including what you would cut.

Done when: the image contains no secret, all configuration comes from the
environment, and you can account for everything the public URL exposes.

## After Part 2

There is no Part 3. You will have built both shapes a system can take — a bounded
single loop and an explicit graph — and the remaining work is domain work rather
than architecture work.
