# Client brief — Meridian Harbour Advisers

The fictional client for the whole programme. Every consultant increment is
written for this firm.

Invented, but built to be realistic: the constraints below are the ones that
actually decide whether an AI capability lands in a mid-sized financial firm.

## The firm

Meridian Harbour Advisers is an independent investment advisory business. It
manages discretionary portfolios for private clients and a handful of small
charitable endowments, and publishes research its advisers use with clients.

| | |
| --- | --- |
| Founded | 1998 |
| Headcount | 412 |
| Offices | Head office plus three regional offices |
| Assets under management | £6.8bn |
| Clients | ~4,100 private clients, 23 endowments |
| Ownership | Partner-owned, 31 equity partners |
| Regulator | Financial Conduct Authority |

## The research desk

The part of the firm this programme concerns.

Eleven people: a head of research, six analysts, two juniors, and two data
specialists shared with operations.

What they produce:

- A weekly market note, circulated internally Monday mornings
- Company notes on the 180-name approved list, each reviewed at least annually
- Ad hoc requests from advisers, typically "what has changed at X since we last
  looked", at around 40 a week
- Quarterly thematic pieces, four a year

The ad hoc requests are the pressure point. They arrive unpredictably, they are
mostly rediscovery of things the desk already knew, and they are what analysts
complain about. Turnaround is two to five days and advisers describe it as the
main friction in client conversations.

## Technology

| | |
| --- | --- |
| Portfolio management | Vendor platform, hosted, limited API |
| CRM | Salesforce |
| Market data | Two vendor terminals, 14 seats, significant annual licence |
| Documents | SharePoint, roughly 20 years of accumulated notes |
| Productivity | Microsoft 365 |
| Cloud | Azure, modest footprint, mostly lift-and-shift |
| IT staff | Nine, including one infrastructure lead and no ML engineers |

No data platform. Research notes live in SharePoint folders with inconsistent
naming. There is no single place that records what the desk currently thinks
about a given company.

## People and politics

The head of research, in post six years, is cautious about AI and specific about
why: she has seen two vendor pilots fail at the firm and believes the risk is
plausible-sounding output reaching a client note unchallenged. She is not
obstructive and she will engage with evidence.

Two of the six analysts are enthusiastic and already use a chatbot informally for
drafting, outside any policy. The two juniors are nervous about what this means
for their roles — their work is the largest share of the rediscovery effort.

The managing partner is supportive in principle and wants a cost number before a
capability demonstration.

Compliance reports to the COO and has not been consulted yet.

## Constraints that will decide this

Client data cannot leave the firm's tenancy without a completed data protection
assessment. There is a process; it takes about six weeks.

Market data vendor licences restrict redistribution and derived works. Nobody at
the firm has read the clauses that would apply to machine consumption.

Anything reaching a client must be attributable and reviewable — an adviser has
to be able to say where a number came from.

FCA Consumer Duty applies. Advice informed by a tool the firm cannot explain is a
regulatory problem, not just a technical one.

IT has no capacity until the next financial year without something being dropped.

There is no AI policy. There is an outsourcing policy from 2019 that compliance
will reach for by default.

## Budget

No allocated budget. The managing partner has indicated that a well-evidenced
case for up to £150k of first-year spend, including people, would get a hearing
at the partner meeting. Anything above that needs a full partner vote.

## What success would look like to them

Not what success looks like to you.

The head of research would call it a success if ad hoc request turnaround dropped
below a day without a single unsourced claim reaching an adviser. The managing
partner would call it a success if the desk absorbed a 20% rise in adviser
demand without a twelfth headcount. The juniors would call it a success if they
spent less time on rediscovery and more on the thematic work.

Those three are not the same objective, and part of your job is noticing that.

---

## Swapping the client

If this firm does not suit your cohort, replace this file and nothing else. The
template, the lenses and the eight increments make no assumptions about the
industry — only that the client has a research or analysis function, a regulator
to answer to, and no spare engineering capacity.
