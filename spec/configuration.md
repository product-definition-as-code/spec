# Configuration

The kernel configuration contract is deliberately small. It standardizes only the repository settings that change how every conforming implementation locates and validates the Product Definition. Tool-specific integrations, generated files, commands and user-interface preferences are not kernel configuration.

## Location and discovery

The configuration file is `.product/config.yaml`. Its containing directory is the **configuration root** and the model repository root for that invocation.

Starting from the invoked path, an implementation MUST inspect that directory and then each parent directory for `.product/config.yaml`; the first file found wins. Discovery stops at the filesystem root. An implementation MUST NOT merge several configuration files. Given the same absolute invoked path and filesystem tree, discovery MUST select the same file.

When no configuration file is found, defaults apply at the enclosing git repository root. Outside a git working tree, an invocation that needs repository configuration fails as invalid configuration with `PRODUCT050`.

Repository-relative paths in this contract resolve from the configuration root, never from the current working directory.

## Versioned document

When present, `.product/config.yaml` MUST be one YAML 1.2 document and MUST validate against [`schemas/v1alpha1/config.schema.json`](../schemas/v1alpha1/config.schema.json). Duplicate mapping keys, aliases, anchors, tags and merge keys are not permitted.

The document has this complete kernel shape:

```yaml
version: v1alpha1
product-root: docs/product
validation:
  warnings-as-errors: false
extensions: {}
```

| Key | Presence | Meaning and default |
| --- | --- | --- |
| `version` | required when the file exists | Configuration serialization version; exactly `v1alpha1`. |
| `product-root` | optional | Repository-relative POSIX path to the Product Definition root; default `docs/product`. |
| `validation` | optional | Kernel validation policy; default `{}`. |
| `validation.warnings-as-errors` | optional | Escalate every normative warning to a failing result; default `false`. |
| `extensions` | optional | Mapping reserved for implementation-specific configuration; default `{}`. |

`product-root` MUST be a normalized, non-empty relative path using `/`. It MUST NOT be absolute, contain `.` or `..` segments, contain an empty segment, use `\`, or resolve outside the configuration root.

Unknown keys outside `extensions` are invalid. Values below `extensions` are opaque to the kernel. An implementation MUST ignore extension namespaces it does not own and MUST NOT emit `PRODUCT050` merely because it does not understand one. Extension configuration MUST NOT change the meaning, severity or emission of a normative diagnostic.

Configuration MUST NOT suppress a diagnostic defined by this specification. `warnings-as-errors` changes the command result for warnings; it does not change their diagnostic `severity`, remove them, or permit selecting individual warning codes. A conforming machine-readable report therefore contains the same diagnostics with the option on or off.

## Invalid configuration

Malformed YAML, unsupported `version`, schema failure, forbidden YAML features, an invalid `product-root`, or an unknown key outside `extensions` produces exactly one `PRODUCT050` against `.product/config.yaml` and exits `2` before artifact discovery or command-specific work.

When the document parsed, `field` is the first invalid instance path in Unicode code-point order. When it did not parse, `field` is absent. `artifact`, `change` and `target` are absent. A command MUST NOT continue with defaults after finding an invalid configuration file.

## Extension boundary

An implementation MAY define its own nested mapping below an extension key it controls, preferably a reverse-DNS name such as `extensions.com.example.tool`. That mapping and its versioning are implementation-defined. No extension key makes an implementation-specific command, integration, generated file or policy part of PDaC conformance.
