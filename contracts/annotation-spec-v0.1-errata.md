# Annotation Specification v0.1 - Errata

## Status

This errata applies to `contracts/annotation-spec-v0.1.md` without changing its semantics or ontology.

## Correction

Validation rule 6 contains a typographical error. The token `projjct_group_id` must be read as `project_group_id`.

The corrected rule is:

```text
1. A dataset split cannot contain the same project_group_id across multiple splits.
```

This correction is non-semantic. It matches the existing project-level dataset leakage-prevention section and the `contracts/annotation-validation-rules-v0.1.json` group key.
