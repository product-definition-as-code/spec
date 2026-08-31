# Artifact templates

One copy-paste file per artifact type, plus the Product Change. Copy the file for the kind you need, replace the ID, fill the sections, and you have a valid PDaC artifact without installing anything.

These templates are **non-normative**, like the diagrams: they exemplify the specification, they do not define it. Where a template and the [Artifacts chapter](../spec/artifacts.md) or the [Product Changes chapter](../spec/product-changes.md) appear to disagree, the chapter wins. Unlike the diagrams, the templates are machine-checked: `scripts/check-templates.mjs` validates every file against the [v1alpha1 schemas](../schemas/v1alpha1) and the required body sections named in the chapters, in CI, so they cannot drift from the normative text.

The files use `EXAMPLE-001` IDs and one small worked domain, meeting room booking, and they reference each other: together they form a miniature product model, so each template also shows the relationships its type carries. The IDs are placeholders by design; an ID is immutable once accepted, so choose yours before the first review.

| Type | Template |
| --- | --- |
| Actor | [actor.md](actor.md) |
| Journey | [journey.md](journey.md) |
| Use Case | [use-case.md](use-case.md) |
| Business Rule | [business-rule.md](business-rule.md) |
| Domain Term | [domain-term.md](domain-term.md) |
| Bounded Context | [bounded-context.md](bounded-context.md) |
| Functional Requirement | [functional-requirement.md](functional-requirement.md) |
| Quality Requirement | [quality-requirement.md](quality-requirement.md) |
| Constraint | [constraint.md](constraint.md) |
| Structured Behaviour | [structured-behaviour.md](structured-behaviour.md) |
| Product Change | [product-change.md](product-change.md) |

pdac.dev renders this directory at [pdac.dev/templates](https://pdac.dev/templates/).
