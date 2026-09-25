# Artifact templates

One copy-paste file per artifact type, plus the Product Change. Copy the file for the kind you need, replace the ID, fill the sections, and you have a valid PDaC artifact without installing anything.

These templates are **non-normative**, like the diagrams: they exemplify the specification, they do not define it. Where a template and the [Artifacts chapter](../spec/artifacts.md) or the [Product Changes chapter](../spec/product-changes.md) appear to disagree, the chapter wins. Unlike the diagrams, the templates are machine-checked: `scripts/check-templates.mjs` validates every file against the [v1alpha1 schemas](../schemas/v1alpha1) and the required body sections named in the chapters, in CI, so they cannot drift from the normative text.

The files use `EXAMPLE-001` IDs and one small worked domain, meeting room booking, and they reference each other: together they form a miniature product model, so each template also shows the relationships its type carries. The IDs are placeholders by design; an ID is immutable once accepted, so choose yours before the first review.

| Type | Template | Reference location |
| --- | --- | --- |
| Actor | [actor.md](actor.md) | `model/actors/` |
| Journey | [journey.md](journey.md) | `model/journeys/` |
| Use Case | [use-case.md](use-case.md) | `model/use-cases/` |
| Business Rule | [business-rule.md](business-rule.md) | `model/business-rules/` |
| Domain Term | [domain-term.md](domain-term.md) | `model/domain/terms/` |
| Bounded Context | [bounded-context.md](bounded-context.md) | `model/domain/bounded-contexts/` |
| Functional Requirement | [functional-requirement.md](functional-requirement.md) | `model/requirements/functional/` |
| Quality Requirement | [quality-requirement.md](quality-requirement.md) | `model/requirements/quality/` |
| Constraint | [constraint.md](constraint.md) | `model/requirements/constraints/` |
| Structured Behaviour | [structured-behaviour.md](structured-behaviour.md) | `model/behaviours/` |
| Product Change | [product-change.md](product-change.md) | `changes/active/<chg-id>/change.md` |

## Where the files live

The specification fixes the two roots, `docs/product/model` for the accepted definition and `docs/product/changes` for its history ([Product Changes → Structure](../spec/product-changes.md#structure)). The directories inside them are the reference layout: the one ProductShape creates, its guides assume, and its dogfooded repositories use. Each file is named by its lowercase ID; the reference implementation warns when the name disagrees (`PRODUCT101`). Two directories do not repeat their type's name: Structured Behaviour files live in `behaviours/`, Domain Term files in `domain/terms/`.

```text
docs/product/
├── changes/
│   ├── active/
│   │   └── chg-example-001/
│   │       ├── change.md
│   │       └── proposed/            # same layout as model/
│   ├── completed/
│   ├── rejected/
│   └── superseded/
└── model/
    ├── actors/act-example-001.md
    ├── journeys/jrn-example-001.md
    ├── use-cases/uc-example-001.md
    ├── business-rules/br-example-001.md
    ├── domain/
    │   ├── terms/term-example-001.md
    │   └── bounded-contexts/bc-example-001.md
    ├── requirements/
    │   ├── functional/fr-example-001.md
    │   ├── quality/qr-example-001.md
    │   └── constraints/con-example-001.md
    └── behaviours/sb-example-001.md
```

pdac.dev renders this directory at [pdac.dev/templates](https://pdac.dev/templates/).
