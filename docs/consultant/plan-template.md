# Transformation plan — section template

Copy this for each sprint's increment. Keep the six headings and their order, so
the eight sections read as one document.

Aim for two pages. A longer section is usually one that avoided a decision.

---

## Sprint N — implementing *[name the artifact]*

**What exists.** Two or three sentences on what was built this sprint, in terms a
client would follow. No framework names unless they matter to the decision.

**The one-line recommendation.** What you would tell the client to do about this
capability now. Lead with it; the rest of the section is why.

### Strategy

Why the firm would do this at all. Which part of what they sell gets better,
faster or cheaper. What they could offer that they cannot today.

Name the alternative you are rejecting — doing nothing, buying a vendor product,
hiring two analysts — and why this beats it. A recommendation with no rejected
alternative has not been thought through.

### Infrastructure and cost

What must exist to run it: compute, data access, network egress, identity and
credentials, storage for anything it keeps.

Then the numbers, from your own ledger rather than estimates:

| | Value | Source |
| --- | --- | --- |
| Cost per run | | ledger |
| Runs per day at real volume | | assumption — state it |
| Monthly run cost | | calculated |
| Other monthly cost | | infrastructure, licences |

State every assumption as an assumption. A client can argue with a stated
assumption and cannot argue with a number that appeared from nowhere.

### Deployment

How it goes from your machine to something people use. Environments, what
"release" means here, how a change gets reviewed, and how you roll back when a
change is wrong.

If the honest answer at this sprint is "it is not deployable yet", say that and
say what the gap is.

### Monitoring

How anyone knows it is working. What signal, seen by whom, how often.

Separate the two kinds: the system is broken (errors, timeouts, cost spikes) and
the system is confidently wrong (bad numbers, weak sourcing, drift). The second
is the hard one and is where most of these programmes fail quietly.

Name the threshold that triggers a human looking.

### People and resources

Who operates it day to day. Whose job changes, and how. What they need to learn,
and how they learn it.

Be concrete about the uncomfortable part: if this absorbs work someone is paid to
do, say so, and say what you would do about it. A plan that hides this gets
found out in the first steering meeting.

What you would hire, if anything, and what you would not.

### Risk and governance

What goes wrong. For each one: likelihood, what it costs, which control catches
it, and who owns that control.

| Risk | Impact | Control | Owner |
| --- | --- | --- | --- |
| | | | |

Include at least one risk that your technical work this sprint introduced rather
than solved. Every capability adds a failure mode, and naming yours is the
difference between a plan and a sales pitch.

### Open questions

What you would need to ask the client before committing to any of the above.
Three to five, each one specific enough to get a usable answer.

---

## A note on tone

Write for a sceptical executive who has been sold AI before. That means: no
adjectives doing the work of evidence, no claimed benefits without a measure,
and an honest account of what this does not do.

The most persuasive section you can write is the one that tells them which part
of your own recommendation you are least sure about.
