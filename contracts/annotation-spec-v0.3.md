# Structural Detection Annotation Specification v0.3 — Active

## Status and authority

Active specification for `column`, `beam`, and `wall`. This specification supersedes annotation-spec v0.2 for new manual-labeling revisions while preserving backward compatibility for existing v0.2 axis-aligned annotations.

Annotations are detector training/evaluation evidence only and MUST NOT create Core entities, engineering coordinates, scale, topology, levels, or final engineering geometry.

## Coordinates and geometry

Annotation coordinates use original `source-page` coordinates in `pdf-point` units with top-left origin, +x right, and +y down.

Every annotation MUST preserve a tight axis-aligned `bbox` envelope.

An annotation MAY additionally preserve an exact oriented rectangle:

```json
{
  "oriented_bbox": {
    "center_x": 5,
    "center_y": 5,
    "width": 10,
    "height": 4,
    "rotation_deg": 0
  }
}
```

Requirements:

- `width` and `height` MUST be finite and greater than zero.
- `rotation_deg` is clockwise screen/source-page rotation in degrees because +y is down.
- Normalize `rotation_deg` to `[-180, 180)`. `0` is the canonical axis-aligned default.
- All four oriented-box corners MUST remain inside the effective source-page bounds.
- The required `bbox` MUST tightly enclose the four `oriented_bbox` corners.
- If `oriented_bbox` is absent, the annotation is interpreted as the v0.2 axis-aligned bbox with zero rotation.
- New annotations using oriented geometry MUST set `annotation_spec_version` to `v0.3`.

## Class rules

### `column`
Annotate the visible plan-footprint graphic whose primary semantic intent is a structural column. Oriented boxes are optional.

### `beam`
Annotate the full visible beam graphic footprint. For rotated beams, an oriented box is preferred over a loose axis-aligned envelope. The box center and long axis are annotation geometry only and MUST NOT be interpreted as engineering centerline or endpoints.

### `wall`
Annotate visible source-drawing graphics whose primary semantic intent is a structural wall. For rotated walls, an oriented box is preferred over a loose axis-aligned envelope.

## User interaction boundary

A labeling tool MAY keep rotation disabled by default to optimize the common zero-rotation case. When the user explicitly enables rotation, the tool MAY expose a rotation handle for any active class. Tool UI state is not part of the annotation contract.

## QA and provenance

Preserve annotation ID, source ID, page ID, project group ID, class, bbox, optional oriented_bbox, annotation spec version, flags, annotator, reviewer, disposition, and audit history.

## Compatibility

- Annotation spec v0.2 remains readable.
- A v0.2 annotation without `oriented_bbox` is equivalent to v0.3 zero rotation.
- Downstream consumers that do not support oriented geometry MAY use the required axis-aligned `bbox` envelope, but MUST NOT delete or silently discard `oriented_bbox` from versioned intake artifacts.
- This specification does not authorize dataset admission or training.
