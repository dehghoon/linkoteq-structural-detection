# Pilot v0.1 Manifest Errata

## Correction

In `datasets/pilot-v0.1/manifest.json`, the `src-p2025-182-croquis` pilot page record for sheet `EsMx401` contains a typographical field name:

```text
"Pae_id": "p03"
```

The field name must be read as:

```text
"page_id": "p03"
```

This is a non-semantic correction. The source, page number, sheet identity, split assignment, target classes, and dataset inventory are unchanged.

## Release gate

Tooling MUST treat `pae_id` as invalid and must not silently accept it as `page_id`. The canonical manifest should be corrected before pilot-v0.1 is approved or used for benchmark/training release claims.
