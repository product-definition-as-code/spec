# The Product Definition as Code Manifesto

AI-assisted engineering has made implementation fast. The limiting factor of software has moved left: from writing code to knowing, precisely and verifiably, what the product is. An agent that writes code in minutes amplifies whatever understanding it is given, including none. We believe product knowledge deserves the discipline we learned to give code, and we have come to value:

**A defined product** over a queue of tickets.

**Explicit change** over casual edits.

**Typed relationships** over organized documents.

**Human judgment** over machine confidence.

That is, while there is value in the items on the right, we value the items on the left more.

## Principles

1. Product knowledge lives in the repository, close to the software it defines.
2. Markdown is the source of truth. The product graph is compiled from it, never authored by hand, and nothing generated is authoritative.
3. Every artifact has a stable, immutable identity.
4. Relationships are explicit, typed and machine-readable. The relationships are the methodology: artifacts without them are just better-organized documents.
5. The baseline changes through exactly one operation: explicit promotion of a verified Product Change by a human. Everything else is a proposal.
6. Uncertainty is a first-class citizen. Open questions are preserved, never resolved by fiat, and no tool or model invents a product decision.
7. Deterministic tools enforce structure. AI does semantic work. Humans decide. The division is not negotiable.
8. Backlog items are projections of product changes, not the source of truth.
9. Delivery consumes product context through a one-way handoff. Implementation may reveal contradictions, but it never silently rewrites the definition.
10. A product definition is worth exactly as much as it can be validated. Given the same files, validation produces the same answer on every machine, every time.

## Signing

The manifesto is signed by pull request: add your name to [SIGNATORIES.md](SIGNATORIES.md).

---

## The position in full

For decades the slowest part of building software was building it. Teams organized everything around that bottleneck: thin tickets, just-in-time specification, product knowledge living in people's heads and in the code, because the code was where all the time went anyway.

AI-assisted engineering changes the constraint. When implementation accelerates, the limiting factor moves left, into questions that were always there but could be answered slowly: What is this product, and who is it for? Which actors interact with it, and what outcomes do they pursue? What behaviour is intended, and which rules govern it? What do our words mean, and where does each meaning hold? Which requirements follow from all of that, and why? When something changes, what else is affected? And when an AI agent implements an increment, what context does it actually need, precisely, and nothing else?

The scarce asset is no longer implementation capacity. It is a product definition worth implementing.

### A backlog is not a product definition

Backlogs are queues of work. They are good at ordering effort and bad at holding knowledge. A user story describes a delivery increment: one step, for one actor, at one moment in the product's history. It says what to add or change next. It does not say what the product *is*. Sum every story ever completed and you still do not get a product definition; you get an archaeology problem. Closed tickets are where product knowledge goes to die.

### An SDD spec is not one either

Spec-Driven Development is a real improvement: it makes an implementation increment explicit, reviewable and verifiable before code is written. We build on it, not against it. But an SDD spec answers a bounded question: how does this one increment change the software? It is scoped to a change, owned by a delivery workflow, and archived when the change ships. What is still missing is the thing the deltas are deltas *of*: a canonical, current, validated description of the product that every increment reads from and, once verified, writes back to.

Product Definition as Code adds that layer in front. Definition first, then change, then slice, then handoff to SDD, then implementation, then verification, then explicit promotion back into the definition. The loop closes.

### Explicit change or nothing

A definition that can be edited casually is a definition nobody can trust. So the baseline is modified by exactly one operation: promotion of a verified Product Change. A change states its delta explicitly, carries complete proposed future-state artifacts, keeps its open questions visible, and is validated as an overlay against the baseline before a human approves it. This is the same discipline that made code trustworthy: no direct pushes to main, every change reviewable as a diff, history that explains itself. Product knowledge deserves the pipeline code already has.

### What this is not

Not a product-management platform: no boards, no workflow engine, no dashboards. Not a graph database: the graph is a compiled artifact of your repository, and if it disappeared nothing would be lost. Not an ontology: the artifact types are a small, opinionated vocabulary for defining products, not a universal knowledge model. Not a roadmapping tool: it says what the product is and how it changes, not when or for which quarter.

### Two names, on purpose

**Product Definition as Code** is the methodology: the long-lived, implementation-independent concept and this normative specification. **[ProductShape](https://github.com/juangcarmona/productshape)** is its reference implementation, exactly as OpenSpec is an implementation of Spec-Driven Development. A methodology can have more than one implementation, and binding the ideas to one tool's name would quietly narrow both.

---

*The founding article is [Product Definition as Code for the AI-SDLC](https://jgcarmona.com/en/product-definition-as-code/) (July 2026). This text is licensed under CC BY 4.0.*
