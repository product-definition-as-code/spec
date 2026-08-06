# The Product Definition as Code Manifesto

AI-assisted engineering has made implementation fast. As implementation cost falls, ambiguity and decision quality become the larger share of delivery risk: the pressure moves left, from writing code to knowing, precisely and verifiably, what the product is. An agent that writes code in minutes amplifies whatever understanding it is given, including none. We believe product knowledge deserves the discipline we learned to give code, and we have come to value:

**A defined product** over a queue of tickets.

**Explicit change** over casual edits.

**Typed relationships** over organized documents.

**Human judgment** over machine confidence.

That is, while there is value in the items on the right, we value the items on the left more.

![Two timelines running at different speeds. The product thinking timeline runs the full width, passing accepted intent and later definition evolves. Below it, a shorter software delivery timeline starts later, passing cited by delivery work and then implementation; an arrow labelled "cited by" drops from accepted intent down onto it. During delivery, new evidence, a false assumption, an uncovered case or a required product decision feed a dashed amber path back up to the product timeline and into a proposed Product Change carrying semantic intent. A summary panel states that definition can lead implementation, with product thinking running ahead of software delivery and a dashed feedback arrow returning.](assets/diagrams/pdac-7-definition-ahead-of-implementation.png)

_Figure PDaC-7 — why should the product definition not trail the code? Non-normative, like the rest of this manifesto._

## Principles

1. Product knowledge lives in a git repository, as files. Co-located with the code when one repository serves; dedicated when many do.
2. Markdown is the source of truth. The product graph is compiled from it, never authored by hand, and nothing generated is authoritative.
3. Every artifact has a stable, immutable identity.
4. Relationships are explicit, typed and machine-readable. The relationships are the methodology: artifacts without them are just better-organized documents.
5. The definition changes through exactly one mechanism: an explicit Product Change, approved by a human and accepted through review. Everything else is a proposal.
6. Uncertainty is a first-class citizen. Open questions are preserved, never resolved by fiat, and no tool or model invents a product decision.
7. Deterministic tools enforce structure. AI does semantic work. Humans decide. The division is not negotiable.
8. Backlog items are projections of accepted product intent, not the source of truth.
9. One-way authority, two-way learning. Delivery consumes canonical product knowledge through citations and reports reality back as proposed Product Changes; a human decides whether to accept them. Delivery never silently rewrites the definition.
10. Validation is deterministic and proves structure, never truth. Given the same files it produces the same answer on every machine, every time; whether the model reflects reality is answered by accountable review and delivery evidence, not by a green check.

## Signing

The manifesto is signed by pull request: add your name to [SIGNATORIES.md](SIGNATORIES.md).

---

## The position in full

For decades the slowest part of building software was building it. Teams organized everything around that bottleneck: thin tickets, just-in-time specification, product knowledge living in people's heads and in the code, because the code was where all the time went anyway.

AI-assisted engineering is changing the constraint. As implementation cost falls, ambiguity and decision quality become a larger share of delivery risk, and the pressure moves left, into questions that were always there but could be answered slowly: What is this product, and who is it for? Which actors interact with it, and what outcomes do they pursue? What behaviour is intended, and which rules govern it? What do our words mean, and where does each meaning hold? Which requirements follow from all of that, and why? When something changes, what else is affected? And when an AI agent implements an increment, what context does it actually need, precisely, and nothing else?

The scarce asset is no longer implementation capacity. It is a product definition worth implementing.

### A backlog is not a product definition

Backlogs are queues of work. They are good at ordering effort and bad at holding knowledge. A user story describes a delivery increment: one step, for one actor, at one moment in the product's history. It says what to add or change next. It does not say what the product *is*. Sum every story ever completed and you still do not get a product definition; you get an archaeology problem. Closed tickets are where product knowledge goes to die.

### An SDD spec is not one either

Spec-Driven Development is a real improvement: it makes an implementation increment explicit, reviewable and verifiable before code is written. We build on it, not against it. But an SDD spec answers a bounded question: how does this one increment change the software? It is scoped to a change, owned by a delivery workflow, and archived when the change ships. What is still missing is the thing the deltas are deltas *of*: a canonical, current, validated description of the product that every increment reads from and, once verified, writes back to.

Product Definition as Code adds that layer in front, and its boundary is delivery, not any one delivery discipline. Definition first, accepted on a canonical branch; then a Product Change stating what should become true and why, validated, applied and accepted by a human; then delivery, whatever builds: an SDD framework, an AI coding agent given citations as its briefing, or a human team receiving a backlog item that finally carries its full context. Then implementation, verification, and a proposed Product Change back into the definition when reality contradicts it. The loop closes, whoever did the building. And it closes under one rule: one-way authority, two-way learning. Delivery never silently rewrites accepted product intent, and everything delivery learns, contradictions, partial results, discovered constraints, flows back as proposed changes. Authority moves in one direction. Information moves in both.

### Explicit change or nothing

A definition that can be edited casually is a definition nobody can trust. So the definition is modified by exactly one mechanism: an explicit Product Change. A change states its delta explicitly, carries complete proposed future-state artifacts, keeps its open questions visible, and is validated as an overlay against the baseline before a human approves it, applies it and accepts it through review. This is the same discipline that made code trustworthy: no direct pushes to main, every change reviewable as a diff, history that explains itself. But a diff shows which files moved, not what the product now means, so the change carries the meaning the diff cannot.

### What validation proves, and what it cannot

Versioning, schemas, graph checks and digests prove that a product model is well-formed, internally consistent and unchanged. They cannot prove that it reflects user needs, business reality, regulatory interpretation or deployed behaviour. A perfectly valid graph can describe the wrong product. Anyone who tells you otherwise is selling ceremony as confidence.

So this methodology distinguishes four questions that a single green check must never collapse:

| Layer | Question it answers | What counts as evidence |
| --- | --- | --- |
| Structural validity | Is the model well-formed under this spec version? | Schema and deterministic graph checks |
| Accepted intent | Has an accountable owner approved this as the current target? | Review, decision record, change and merge history |
| Delivery correspondence | Is the target implemented, deployed or verified in a named environment? | Attested claims, tests, release evidence |
| Outcome validity | Did the change produce the expected result? | Experiments, telemetry, research |

Tooling in this methodology guarantees the first layer, records the second, and gives the third and fourth a place to land as evidence. It never claims them for free.

### A kernel, a profile, a workflow

Three things travel under this name, and they have different weights.

The kernel is the part worth standardizing: stable immutable identity, typed relationships authored once and compiled into a graph, an accepted definition that changes only through explicit, validated changes, deterministic structural validation with stable codes, and verifiable citations that bind consumer documents to canonical product text. Small, formal, testable by conformance.

The artifact vocabulary, actors, journeys, use cases, business rules, domain terms, bounded contexts and requirements, is the reference profile. It is opinionated, it is a good default, and it is not the essence. A team that models with events, or pure domain-driven design, or a regulated obligation catalogue, should be able to bring its own profile and still conform to the kernel.

The change flow, propose (a Product Change), validate (overlay), apply, accept (human review), cite (consumer), verify (citations), is the reference workflow. It is the governance we recommend and practice. It is one way to operate the kernel, not the definition of it.

Confusing these three layers is how methodologies die: the kernel gets dismissed because the profile looks like old ideas, or the workflow's ceremony gets mistaken for the price of entry. The layers exist so that experts can replace the outer two and keep the part that matters.

### What this is not

Not a product-management platform: no boards, no workflow engine, no dashboards. Not a graph database: the graph is a compiled artifact of your repository, and if it disappeared nothing would be lost. Not a universal ontology or a semantic-web platform: PDaC defines a bounded, opinionated vocabulary for product definition, with typed relationships and closed validation, not a universal knowledge model. Not a roadmapping tool: it says what the product is and how it changes, not when or for which quarter. Not a truth machine: validation proves structure, not correctness, and the model is inspectable, never automatically true. And not a replacement for discovery: interviews, research, experiments, strategy and product judgment happen before and around this methodology; it operationalizes the decisions those activities produce, it does not produce them.

### Two names, on purpose

**Product Definition as Code** is the methodology: the long-lived, implementation-independent concept and this normative specification. **[ProductShape](https://github.com/juangcarmona/productshape)** is its reference implementation, exactly as OpenSpec is an implementation of Spec-Driven Development. A methodology can have more than one implementation, and binding the ideas to one tool's name would quietly narrow both.

---

*The founding article is [Product Definition as Code for the AI-SDLC](https://jgcarmona.com/en/product-definition-as-code/) (July 2026). This text is licensed under CC BY 4.0.*
