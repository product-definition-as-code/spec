<p align="center"> <img src="https://raw.githubusercontent.com/product-definition-as-code/.github/main/profile/pdac-social-banner.png" alt="PDaC: Product Definition as Code" width="720" /> </p>

# The PDaC Specification

**The normative specification of Product Definition as Code (PDaC).**

<!-- canonical-pdac-definition:start — copy verbatim or link; see CONTRIBUTING.md, "Agreed wording" -->

Product Definition as Code keeps the agreed product definition in versioned Markdown that delivery work cites instead of restating.

The definition lives as small, related Markdown files — actors, journeys, use cases, business rules, domain terms, requirements — compiled into a validated product graph that humans and AI agents read alike. It changes only through an explicit Product Change, reviewed and accepted by a human. Consumer documents (SDD specs, tasks, agent prompts) cite the exact product text they rely on by stable ID and content digest, and when cited text changes, tools flag every recorded citation for review: documentation drift is detected instead of silent. Deterministic tools check structure and references, never truth; people decide what is true and what should change.

<!-- canonical-pdac-definition:end -->

Shown with ProductShape, the reference implementation of Product Definition as Code:

```console
$ prodshape citations verify
stale	BR-REFUND-001	openspec/checkout-flow.citations.yaml:1
warning PRODUCT061 openspec/checkout-flow.citations.yaml [BR-REFUND-001]: Citation of 'BR-REFUND-001' is stale: canonical content changed since the citation was recorded
1 citation(s): 0 current, 1 stale, 0 tampered, 0 unresolved
```

That is the citation contract, the delivery boundary of PDaC — an open methodology for the upstream layer of the AI-SDLC. Those citations brief a Spec-Driven Development framework, an AI coding agent, or a human team. [See it in 30 seconds on pdac.dev](https://pdac.dev/).

This repository holds the Product Definition as Code specification, the manifesto and the conformance tests — implementation-independent by design: contracts, not commands.

<p align="center"> <img src="assets/diagrams/pdac-0-one-minute-map.png" alt="Two zones. On the left, product thinking: what the product means, holding the accepted product definition, versioned, related and reviewable. On the right, software delivery: how the product is built, holding SDD specs, AI agents, developers, backlog and code. An arrow labelled 'cited by' runs from the definition to delivery, and a dashed amber arrow returns, labelled 'delivery evidence reveals new product questions or changes'." width="720" /> </p>

<p align="center"><em>PDaC-0 - what is PDaC, in one minute? <a href="https://pdac.dev/diagrams/">All nine diagrams</a>.</em></p>

## Status

**v0.1 (request for comments), extraction in progress.** First published 2026-08-07: this is an early draft, not a near-final standard. The honest picture of every surface, the version dimensions and the gates to v1 are in [MATURITY.md](MATURITY.md); what the methodology cannot claim yet is in [known limits](https://pdac.dev/known-limits/).

The specification text is being extracted from the [reference implementation](https://github.com/juangcarmona/productshape), where it was developed and validated against a self-hosted product model. During extraction, chapters may still contain references to repository layouts or behaviors of the reference implementation; each is being generalized or removed. v1.0 freezes after a public comment period.

| Milestone | State |
| --- | --- |
| Chapters extracted | In progress |
| Conformance tests (complete, normative set) | In progress; the published cases run today via [pdac-lint](https://www.npmjs.com/package/pdac-lint) |
| Public comment period (v0.1) | Planned |
| v1.0 freeze | Planned |

## Contents

The specification lives in [`spec/`](spec/index.md): nine normative chapters, terminology to conformance.

The founding position is [the manifesto](MANIFESTO.md), which you can [sign](SIGNATORIES.md).

## Implementations

| Implementation | Language | Status |
| --- | --- | --- |
| [ProductShape](https://github.com/juangcarmona/productshape) | TypeScript | Reference implementation, v0.x, self-hosted |

The specification wants more than one implementation. If you are building one, open an issue; the [conformance chapter](spec/conformance.md) and the published conformance tests define what "conformant" means (they are not yet a complete normative set). See [IMPLEMENTATIONS.md](IMPLEMENTATIONS.md) for listing criteria.

## Contributing

Changes to the specification go through the [RFC process](CONTRIBUTING.md), which also records the [agreed cross-repo wording](CONTRIBUTING.md#agreed-wording). Governance, maintainers and decision rules are in [GOVERNANCE.md](GOVERNANCE.md). Adopters can add themselves to [ADOPTERS.md](ADOPTERS.md).

## License

The specification text and the manifesto are licensed under [CC BY 4.0](LICENSE.md). Code samples and conformance fixtures are licensed under Apache 2.0.
