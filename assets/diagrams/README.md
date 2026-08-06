# PDaC diagrams

The canonical home for the explanatory diagrams. This directory is the only place these files live; every other surface references them rather than holding a copy.

## Status

The diagrams are **non-normative**. They explain the methodology; they do not define it. Where a diagram and the specification appear to disagree, [the specification wins](../../spec/index.md).

Their arrows are readable prose rather than the canonical relationship vocabulary, and some point in the derived (reverse) direction. The authored relationships are defined in [Relationships](../../spec/relationships.md) and nowhere else.

## How they are consumed

| Surface | Reference |
| --- | --- |
| This repository, on GitHub | Relative path, e.g. `../assets/diagrams/pdac-0-one-minute-map.png` |
| pdac.dev | `/diagrams/<file>`, copied and rewritten by the website's `scripts/sync-spec.mjs` |
| Anywhere else | `https://pdac.dev/diagrams/<file>` |

Nothing is ever re-uploaded to another host. A diagram that needs to appear somewhere new gets a reference, not a copy.

## The set

| File | Question it answers |
| --- | --- |
| `pdac-0-one-minute-map.png` | What is PDaC, in one minute? |
| `pdac-1-product-definition-context.png` | What is inside PDaC and what is outside? |
| `pdac-2-product-definition-model.png` | What does it mean to define the product? |
| `pdac-3-source-to-graph.png` | How is the graph obtained from Markdown? |
| `pdac-4-product-change.png` | How does the accepted definition change? |
| `pdac-5-citation-and-drift.png` | How does PDaC connect to SDD without replacing it? |
| `pdac-6-impact-analysis.png` | What happens when one part of the product changes? |
| `pdac-7-definition-ahead-of-implementation.png` | Why should the product definition not trail the code? |
| `pdac-8-verification-derivation-and-continuity.png` | How do we know the implementation still satisfies the accepted definition? |

## Conventions

File names are lowercase kebab-case, prefixed `pdac-<n>-`, matching the diagram number. The number is part of the identity: `PDaC-6` is referred to by number in prose and in captions.

Each embedded figure carries a caption naming the question it answers, its non-normative status, and the chapter that is authoritative for its subject.

## Changing a diagram

There are no vector sources. A correction means regenerating the PNG upstream and replacing the file here under the same name, so that every reference picks it up. Re-run the optimization below before committing; the unoptimized exports are roughly ten times larger.

```
sharp(src).png({ palette: true, colors: 128, dither: 0, effort: 10 })
```

`dither: 0` is load-bearing. At the default the whiteboard grid dithers into noise that triples the file size for no visual gain.

## Licence

[CC BY 4.0](../../LICENSE.md), as with the rest of the specification text.
