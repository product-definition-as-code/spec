# RFC 0000: Impact polarity in the canonical relationship vocabulary

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-28
- **Proposed target:** PDaC specification 0.2.0; no schema, diagnostic or serialization-version change

## Problem

[Relationships → Canonical vocabulary](../spec/relationships.md#canonical-vocabulary) fixes the authoring direction of every relationship: which artifact type authors it, in which field, at which allowed targets. It says nothing about which end of a relationship is put in question when the other end changes. Authoring direction and impact direction are not the same, and the specification currently only states the first.

The gap is already producing wrong guidance. [Product Changes → Elaboration](../spec/product-changes.md#elaboration) says implementations SHOULD surface "the artifacts a proposed operation would affect, the artifacts that reference them, and the open questions the change has not answered". "The artifacts that reference them" describes a reverse walk over authored edges. `applies-to` is authored on the Business Rule, Quality Requirement or Constraint and points at what it governs, so when a Quality Requirement effectively changes, the use cases it constrains are its **outbound** targets and no reverse walk reaches them. An implementation can follow this SHOULD exactly and still fail to surface the artifacts most obviously in question.

The same gap makes it impossible to state what an impact walk is without each implementation inventing its own. Every consumer of the graph, whether an elaboration assistant, an inspection command or a generated projection, has to decide per field which direction impact flows, and nothing in the specification makes two implementations decide alike.

## Proposal

The canonical vocabulary gains a fourth column, `Polarity`, with three values.

**`dependency`.** The source cites what it builds on. A change to the target puts the source in question. A change to the source says nothing about the target.

**`governance`.** The edge couples both ends. The governed artifact must be reconsidered when the governing artifact changes, and the governing artifact's continued applicability must be reconsidered when the governed artifact changes.

**`none`.** The field carries no impact polarity. Product Change operation edges record a proposal, not a dependency between Product Artifacts.

A relationship field added to this vocabulary MUST declare its polarity.

Polarity is a property of the relationship. It places no obligation on an author and adds no diagnostic. What an implementation does with it is stated in [Product Changes → Elaboration](../spec/product-changes.md#elaboration).

### The table

| Source                 | Field                      | Allowed targets                                             | Polarity   |
| ---------------------- | -------------------------- | ----------------------------------------------------------- | ---------- |
| Journey                | `primary-actor`            | Actor                                                       | dependency |
| Journey                | `steps[].use-case`         | Use Case                                                    | dependency |
| Use Case               | `primary-actor`            | Actor                                                       | dependency |
| Use Case               | `supporting-actors`        | Actor                                                       | dependency |
| Use Case               | `bounded-context`          | Bounded Context                                             | dependency |
| Use Case               | `governed-by`              | Business Rule                                               | dependency |
| Use Case               | `uses-terms`               | Domain Term                                                 | dependency |
| Business Rule          | `applies-to`               | Journey, Use Case, Bounded Context                          | governance |
| Business Rule          | `uses-terms`               | Domain Term                                                 | dependency |
| Domain Term            | `defined-in`               | Bounded Context                                             | dependency |
| Domain Term            | `uses-terms`               | Domain Term                                                 | dependency |
| Functional Requirement | `derived-from`             | Use Case, Business Rule, Constraint                         | dependency |
| Functional Requirement | `verification[].scenario-ref` | Structured Behaviour                                     | dependency |
| Functional Requirement | `uses-terms`               | Domain Term                                                 | dependency |
| Quality Requirement    | `applies-to`               | Journey, Use Case, Bounded Context                          | governance |
| Quality Requirement    | `verification[].scenario-ref` | Structured Behaviour                                     | dependency |
| Quality Requirement    | `uses-terms`               | Domain Term                                                 | dependency |
| Constraint             | `applies-to`               | Journey, Use Case, Bounded Context; absent = entire product | governance |
| Constraint             | `uses-terms`               | Domain Term                                                 | dependency |
| Structured Behaviour   | `illustrates`              | Use Case, Business Rule, Constraint                         | dependency |
| Structured Behaviour   | `uses-terms`               | Domain Term                                                 | dependency |
| Product Change         | `operations.add`           | any product artifact (new ID)                               | none       |
| Product Change         | `operations.modify`        | any existing product artifact                               | none       |
| Product Change         | `operations.remove`        | any existing product artifact                               | none       |

Two assignments are worth stating rather than reading off the table.

`Structured Behaviour.illustrates` is `dependency`. The behaviour cites what it illustrates, so a changed use case, rule or constraint puts the behaviour in question, and a changed behaviour does not put the rule in question. This keeps the specification consistent with itself: [Relationships → Knowledge warning relationship sets](../spec/relationships.md#knowledge-warning-relationship-sets) already states that an incoming `Structured Behaviour.illustrates` relationship MUST NOT count as a consumer for `PRODUCT105`. The specification has already declined to make that edge load bearing in the reverse direction.

`verification[].scenario-ref` is `dependency` on both requirement kinds. The requirement cites the behaviour as its verification, so a changed behaviour puts the requirement in question. See the alternatives.

### Elaboration

The middle clause of the second paragraph of [Product Changes → Elaboration](../spec/product-changes.md#elaboration) is replaced. It currently reads "the artifacts that reference them". It becomes "the artifacts put in question by those artifacts under the impact polarity of [Relationships → Canonical vocabulary](relationships.md#canonical-vocabulary)".

The paragraph stays a SHOULD and the rest of it, including "This is assistance, not authority", is unchanged. What changes is that the SHOULD now has one answer rather than one per implementation.

## Impact

- **On existing conformant repositories:** none. No frontmatter, schema or document validity is affected.
- **On existing implementations:** an implementation that offers elaboration assistance walks the declared polarity rather than a reverse-only view. This is a correction to a SHOULD, not a new obligation; an implementation that offers no elaboration assistance is unaffected.
- **On schemas and serialization:** none.
- **On diagnostics:** none. No code is added, renamed or redefined.
- **On the conformance tests:** none. The column governs a SHOULD with no diagnostic, and no fixture can exercise it under the case convention, exactly as no fixture exercises the elaboration guidance it corrects. This is stated here so the absence is a recorded decision rather than an omission.

## Alternatives considered

### Leave it to RFC 0082 in v0.3

Rejected. [RFC 0082](https://github.com/product-definition-as-code/spec/pull/82) needs this column and originally carried it, but the rest of that RFC is three diagnostic codes, a frontmatter ledger with two digest pins, a staged apply order and fifteen fixtures, and it is still being revised. The elaboration defect is live in v0.2 and its fix carries none of that cost. Publishing the column first also lets an implementation build the walk before a gate exists that fails on it.

### Raise Elaboration to a MUST and add a diagnostic

Rejected here, deliberately. That is RFC 0082's apply gate, and it belongs with the acknowledgment ledger that makes the obligation satisfiable. A MUST with nothing to satisfy it, or a diagnostic with no way to dispose of it, would be worse than the SHOULD it replaced.

### Derive polarity from the field name

Rejected. It happens to work today, since all three `governance` rows are named `applies-to`, but it is a coincidence of the current vocabulary rather than a rule. A future governance field under another name would silently acquire the wrong polarity. The column states the property; the name does not.

### Derive polarity from reachability

Rejected. [Relationships → Reachability](../spec/relationships.md#reachability) is deliberately undirected, which is correct for asking whether a requirement is connected to an actor and useless for asking which end of an edge a change puts in question. Reusing it would make every neighbour of a changed artifact a candidate.

### Treat `verification[].scenario-ref` as governance

Rejected, and it is the closest call in the table. The argument for `governance` is real: if a Functional Requirement changes, the Structured Behaviour cited as its verification may no longer verify it, which is a coupling in both directions. The argument against is that `governance` is reserved for an edge that asserts scope over the other end, which is what `applies-to` does and what a verification reference does not: it names evidence. Recording it as `dependency` keeps the two categories meaning what they say. If real use shows verification adequacy needs its own reconsideration, that is a narrower change than widening `governance` to cover it.

## Decision record

Pending human acceptance under [CONTRIBUTING.md](../CONTRIBUTING.md). This RFC states a property of relationships the specification already defines, and corrects one clause of existing guidance. It adds no obligation on a repository, no schema, no diagnostic and no conformance case.
