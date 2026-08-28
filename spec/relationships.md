# Relationships

The relationships are the methodology: they connect intent (actors), behaviour (journeys, use cases), knowledge (rules, terms, contexts) and obligations (requirements), and they carry traceability through Product Changes.

![Impact analysis over a small graph neighbourhood, before and after a change. Before: BR-REFUND-001 connects to UC-REFUND-002, which is cited by an SDD spec and appears in JRN-CUSTOMER-001, which involves ACT-CUSTOMER-001. After: modifying BR-REFUND-001 walks the relationships to reach the affected product artifacts and the affected citations, each drawn with a dashed amber border labelled affected or stale. The closing line reads: PDaC detects impact, consumers decide what to do.](../assets/diagrams/pdac-6-impact-analysis.png)

_Figure PDaC-6 - what happens when one part of the product changes? Non-normative: the arrows are readable prose and some point in the derived direction. The canonical vocabulary below is authoritative._

## Canonical vocabulary

Every relationship has exactly one canonical direction: it is authored on one artifact type, in one frontmatter field, targeting an allowed set of types.

| Source                 | Field                      | Allowed targets                                             |
| ---------------------- | -------------------------- | ----------------------------------------------------------- |
| Actor                  | `uses-terms`               | Domain Term                                                 |
| Journey                | `primary-actor`            | Actor                                                       |
| Journey                | `steps[].use-case`         | Use Case                                                    |
| Journey                | `uses-terms`               | Domain Term                                                 |
| Use Case               | `primary-actor`            | Actor                                                       |
| Use Case               | `supporting-actors`        | Actor                                                       |
| Use Case               | `bounded-context`          | Bounded Context                                             |
| Use Case               | `governed-by`              | Business Rule                                               |
| Use Case               | `uses-terms`               | Domain Term                                                 |
| Business Rule          | `applies-to`               | Journey, Use Case, Bounded Context                          |
| Business Rule          | `uses-terms`               | Domain Term                                                 |
| Domain Term            | `defined-in`               | Bounded Context                                             |
| Domain Term            | `uses-terms`               | Domain Term                                                 |
| Bounded Context        | `uses-terms`               | Domain Term                                                 |
| Functional Requirement | `derived-from`             | Use Case, Business Rule, Constraint                         |
| Functional Requirement | `verification[].scenario-ref` | Structured Behaviour                                     |
| Functional Requirement | `uses-terms`               | Domain Term                                                 |
| Quality Requirement    | `applies-to`               | Journey, Use Case, Bounded Context                          |
| Quality Requirement    | `verification[].scenario-ref` | Structured Behaviour                                     |
| Quality Requirement    | `uses-terms`               | Domain Term                                                 |
| Constraint             | `applies-to`               | Journey, Use Case, Bounded Context; absent = entire product |
| Constraint             | `uses-terms`               | Domain Term                                                 |
| Structured Behaviour   | `illustrates`              | Use Case, Business Rule, Constraint                         |
| Structured Behaviour   | `uses-terms`               | Domain Term                                                 |
| Product Change         | `operations.add`           | any product artifact (new ID)                               |
| Product Change         | `operations.modify`        | any existing product artifact                               |
| Product Change         | `operations.remove`        | any existing product artifact                               |

A relationship referencing an unknown ID, or targeting a type outside the allowed set, is a validation error.

Array-member relationship fields use the `[]` attribution convention. Diagnostics for a `scenario-ref` relationship MUST report `field` as `verification[].scenario-ref`, just as a Journey step relationship reports `steps[].use-case`. Schema diagnostics such as `PRODUCT002` continue to report their own instance paths.

## Derived relationships

Reverse relationships are always derived by the graph compiler and MUST NOT be authored or manually maintained.

The canonical/derived split is decided once per pair. The load-bearing case:

- **`Domain Term.defined-in` is canonical. `Bounded Context.owns-terms` is derived.** A bounded context's owned terms are exactly the domain terms whose `defined-in` references it. `owns-terms` MUST NOT appear in authored bounded-context frontmatter; schemas reject it. Tools MAY display `owns-terms` in inspection output and generated indexes as a derived field.

All other reverse views (`Actor ← journeys`, `Business Rule ← governed use cases`, `Use Case ← derived requirements`, Requirements verified by a Structured Behaviour, and so on) follow the same rule: derived, displayed, never authored.

## Status interactions

- An `active` artifact MUST NOT reference a `retired` artifact (error).
- An `active` artifact referencing a `deprecated` artifact SHOULD produce a warning.
- `draft` artifacts MAY reference `draft` artifacts.

## Reachability

Some diagnostics depend on _reachability_, defined deterministically as follows: two artifacts are connected if a path exists between them in the undirected view of the product graph restricted to the canonical product relationships above, excluding Product Change edges. A requirement is _reachable from an actor_ when it is connected to at least one Actor node under this definition.

Structured Behaviour edges participate under the same rule. A Requirement verified by a Structured Behaviour is connected to the behaviour's source Use Cases, Business Rules and Constraints. Structural impact analysis therefore includes changes to a Structured Behaviour through those authored edges, without making a semantic impact claim.

## Knowledge warning relationship sets

For `PRODUCT105`, a non-retired Business Rule is consumed if and only if it has at least one valid outgoing `Business Rule.applies-to` relationship, incoming `Use Case.governed-by` relationship or incoming `Functional Requirement.derived-from` relationship, and the artifact authoring that relationship is non-retired. An incoming `Structured Behaviour.illustrates` relationship MUST NOT count as a consumer.

`uses-terms` is authored from an artifact whose interpretation requires a Domain Term to that Domain Term. Reverse views are derived and MUST NOT be authored. A Domain Term MAY author `uses-terms` for a definitional dependency; cycles are not prohibited by this relationship alone.

For `PRODUCT106`, a non-retired Domain Term is used if and only if it has at least one valid incoming `uses-terms` relationship authored by a non-retired Actor, Journey, Use Case, Business Rule, Domain Term, Bounded Context, Functional Requirement, Quality Requirement, Constraint or Structured Behaviour. A prose occurrence, a generated reverse relationship or another relationship path does not count.
