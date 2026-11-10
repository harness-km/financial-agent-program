# The consultant track

Every second week, a two-hour session separate from the build sessions. It is
also the sprint boundary.

The question is always the same, and it is always about what you have just
built: **we now have this. What would it take for a real company to actually run
it?**

Not what it could become. Not the roadmap. What this thing, as it stands at the
end of this sprint, would demand of a firm's infrastructure, budget, people and
controls.

## Why it is a separate session

Because switching between a developer's head and a consultant's head mid-session
does neither well. In the build session the question is "why does my loop not
terminate". Here it is "who gets paged when this breaks at month end". Those are
different modes of attention and they deserve their own two hours.

## Why it is retrospective

A forward-looking plan written before anything exists is a wish list. By
anchoring each increment to an artifact you built and can demonstrate, the
implications stop being generic. "What does it cost to run" is an abstract
question in week 1 and a specific one in week 6, when you have a ledger with
real numbers in it.

It also means you are never speculating about the technology. You know exactly
what it does and does not do, because you built it.

## The six lenses

The same six, in the same order, every sprint. That consistency is what turns
eight sessions into one document rather than eight essays.

| Lens | The question |
| --- | --- |
| Strategy | Why would the firm do this at all? What does it change about what they can offer or compete on? |
| Infrastructure and cost | What has to exist to run it? What does a run cost, and what does the monthly bill look like at real volume? |
| Deployment | How does it get from built to running, and how does it change safely once people depend on it? |
| Monitoring | How does anyone know it is working? How do they find out when it is not, and how fast? |
| People and resources | Who operates it? Whose work changes? What do they need to learn, and who do you have to hire? |
| Risk and governance | What goes wrong, who is accountable when it does, and which control catches it first? |

Not every lens is equally heavy every sprint. Say so when one is thin rather than
padding it — a one-line answer with a reason is a better consulting instinct
than a paragraph of filler.

## The eight increments

Each names the artifact it is reasoning about.

| Sprint | What exists at this point | The implementation question |
| --- | --- | --- |
| 1 | An LLM that can call one tool | What does it take to let a model call our systems at all? Model choice, vendor dependency, what data leaves the building, who holds the keys, own-versus-rent |
| 2 | A single agent answering multi-step questions over three data sources | Which analyst task does this actually touch? Where does it run, how are per-tool credentials held, what sits between a script and something an analyst uses on a Tuesday, how do we know an answer was wrong |
| 3 | An agent that survives long sessions, with behaviour in editable files | Non-engineers can now change what it does. Who is allowed to? Is a prompt edit a production change? Config as code, change control, and who watches the bill |
| 4 | A measured agent: traces and an eval score | Now it can be proposed to a board. What measure would they accept? Who owns the eval set and keeps it current? How do we avoid shipping a worse version? Traces are evidence — and a retention liability |
| 5 | A graph, and a research pipeline hitting the live web | The system now depends on the open internet. Source policy, allowlists, terms of use, outbound network, rate limits. And the live architecture decision: one agent or several, with a cost attached |
| 6 | Parallel section research with relevance filtering and citations | Can the firm stand behind an output in front of a client? Provenance per claim, concurrency cost, and the reviewer role that has just appeared |
| 7 | Critics, an approval gate, and MCP exposing our own agent as a tool | A human approval step is a workflow with an owner, an SLA and an escalation path. MCP puts third-party code inside the trust boundary. Who approves, on what information, and what happens when they are on leave |
| 8 | Verified structured decisions, containerised and deployed | The whole thing in production. Environments, rollback, secrets, on-call. Accountability for a decision the system produced. And adoption: how people start using it, and what happens to those who do not |

## What you produce

One section per sprint, following `plan-template.md`, written for the client in
`company-brief.md`. Eight sections by week 16, presented whole at each release.

Write it as something you would hand a client, not as coursework. Specifics,
numbers, named roles, and open questions you would need answered. "We would need
monitoring" is not an answer; "a daily cost report to the desk head, alerting
above £X a day, and a weekly sample of ten outputs reviewed by a senior analyst"
is.
