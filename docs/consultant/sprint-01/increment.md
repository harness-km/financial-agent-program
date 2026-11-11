---
kind: consultant
week: "02"
sprint: "1"
title: a model that can call one tool
---

## The artifact

Four modules and one notebook. A hand-written tool schema goes to a hosted model,
the model replies asking for `get_latest_close("AAPL")`, your code validates that
request and decides whether to honour it, your tool reads a committed JSON file,
and a ledger records what the exchange cost. One turn, no loop, no framework.

Demo it before you write a word of this section. The whole value of the
consultant track is that you are reasoning about something you have run.

## The question

What would it take for Meridian Harbour Advisers to let a model call their systems
at all?

Not the research agent. Not the roadmap. This: one hosted model, one tool, one
credential, one request leaving the building. Everything in sprints 2 to 8 assumes
the firm has already said yes to that, and nobody has asked them yet.

## What you have as evidence

More than you would expect from one week, and you should use the numbers rather
than adjectives:

- Your ledger row: model, calls, tokens in, tokens out, cost for one exchange
- The actual request body, which shows precisely what left your machine
- `company-brief.md`, for the constraints you are arguing inside

The brief gives you the volume to scale that ledger row against: around forty ad
hoc adviser requests a week, turnaround two to five days. That is the number to
put through the Infrastructure and cost lens. Most consulting on AI stops at
"token costs are low" — you can show the arithmetic.

## Where the weight is this sprint

Two lenses carry this one. Say so, and keep the others short rather than padding
them. `plan-template.md` asks for the six in order; a one-line answer with a
reason is the better instinct.

### Heavy: Infrastructure and cost

Own versus rent is the decision, and it is the first real one in the programme.
A hosted model means per-token cost, a vendor dependency, and prompts leaving the
tenancy. A self-hosted model means capacity the firm does not have — nine IT
staff, no ML engineers, no capacity until the next financial year without
something being dropped.

Work the numbers from your own ledger: cost per exchange, exchanges per request,
requests per week, monthly bill. Then the comparison the managing partner will
actually ask for, which is against the two vendor terminals at fourteen seats and
a significant annual licence. State every assumption as an assumption.

### Heavy: Risk and governance

This is where week 2's security criterion becomes a client-facing argument. You
built three things: validation of the model's output before acting on it, a
refusal path that cannot be mistaken for an answer, and a credential that is
never a function parameter. Each maps to a control the firm would need.

The constraints that decide it are in the brief and none of them are technical:
client data cannot leave the tenancy without a data protection assessment that
takes six weeks; there is no AI policy, only a 2019 outsourcing policy that
compliance will reach for by default; and compliance has not been consulted at
all. Name who owns the key, who can see what was sent, and what the firm's answer
is when an adviser asks whether a client's name went to a third party.

Note the one thing your demo does not establish: your tool read a committed file.
Nothing client-identifying has left anywhere yet. Be honest that the hard version
of this question arrives in sprint 2, when the tool reaches a real system.

### Thin: Deployment and Monitoring

The honest answer is that this is a notebook and is not deployable. Say that, say
what the gap is, and move on in three sentences. A consultant who writes a page
about deploying a notebook has told the client they cannot tell the difference.

Monitoring is thinner still: there is one call and nothing running. The one thing
worth naming is that the ledger exists from week 2 and is the beginning of cost
monitoring, which is the lens that gets heavy in sprint 3.

### Strategy and People

Strategy: why would the firm do this at all, and what is the alternative you are
rejecting — doing nothing, buying a vendor research product, hiring a twelfth
analyst. The brief tells you what success means to three different people and
notes that those three objectives are not the same. Pick whose definition you are
optimising for and say so.

People: the head of research is cautious about AI and specific about why — two
failed vendor pilots, and a belief that the risk is plausible-sounding output
reaching a client note unchallenged. She will engage with evidence. Two analysts
already use a chatbot informally, outside any policy, which is a governance fact
rather than a people fact and belongs in both lenses.

## The gap

Required, per `docs/consultant/README.md`. One thing the firm needs that this does
not do, specific and traceable to the brief.

The obvious one for this sprint: the desk's pressure point is forty requests a
week that are mostly rediscovery of what the desk already concluded, and this
capability answers questions from public data rather than from the firm's own
notes. It could reduce the effort per request without reducing the number of them.

Use that one if you want, but a better section finds its own.

## Deliberately not in scope

- **A roadmap.** The question is what this artifact demands, not what it could
  become. Sprints 2 to 8 each get their own section.
- **Architecture diagrams.** The firm has not agreed to the premise yet.
- **A vendor comparison matrix.** One paragraph on own-versus-rent with a number
  attached beats a table of eight providers.
- **Security as its own section.** It is the Risk and governance lens, as it is
  every sprint.

## What you submit

One section, following `plan-template.md`, in the transformation plan for
Meridian Harbour. Aim for two pages. Due at the sprint boundary, which is this
week.

It is Definition of Done item 6, and the code half and the organisation half of
this programme are the same deliverable.

## Reading

- `docs/consultant/company-brief.md` — all of it, before you start. The
  constraints section and the budget decide most of what you can argue.
- `docs/consultant/plan-template.md` — the six headings and what each asks for.
- Your own ledger row and request body. They are the only primary sources you
  have this sprint, and they are better than anything you could cite.
