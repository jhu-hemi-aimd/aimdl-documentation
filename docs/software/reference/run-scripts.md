---
title: "Run-script reference"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 6 months
safety_level: operational
tags: [software, controls]
---

# Run-script reference

New scripts use a JSON object with `schema_version: 2` and a nonempty ordered `instructions` array. Each instruction is a two-item array: a logical station key and an input object. Every selected sample follows that instruction sequence.

```json
{
  "schema_version": 2,
  "instructions": [
    ["coord", {}],
    ["maxima", {
      "sample": {
        "points": {"frame": "sample", "units": "mm", "values": [[5, 5]]}
      },
      "collection_settings": {"calibrate": false, "collection_mode": "XRD", "count_time": 10, "detector_distance": 0},
      "xray_settings": {"current": 4.375, "voltage": 160, "beam_x": 120, "beam_y": 120}
    }]
  ]
}
```

The numbers above illustrate the schema using supplied values. Confirm them against the station's approved experiment configuration before execution. [Download complete examples](../examples/index.md).

## Shared structure

| Field | Meaning and validation |
| --- | --- |
| `schema_version` | Must be 2 for new uploads and new runs |
| `instructions` | Nonempty list, in execution order |
| Instruction item 0 | One of `helix`, `maxima`, `sphinx`, `profile`, `engrave`, `coord`; only four controllers are supplied here |
| Instruction item 1 | JSON object of station arguments |
| `sample.points.frame` | `sample_holder`, `sample`, or HELIX-only `flyer_grid` |
| `sample.points.units` | Physical points require `mm` or `cm`; omit for `flyer_grid` |
| `sample.points.values` | Nonempty list of numeric pairs; finite, non-Boolean values; flyer-grid values must be integers |

AIMDDS rejects legacy fields such as `scan_points` or `pulse_points` inside `sample`. A missing station-specific settings object may pass central validation and trigger controller defaults, so provide intended inputs explicitly. Refer to the controller pages for defaults, clamping and ignored fields.

COORD accepts only `photo_only` (Boolean) or an empty input object. It does not accept sample coordinates, calibration or persistence options in the script.

## Identity and runtime metadata

Do not include run ID, instruction number, sample database ID or IGSN as controller arguments in a script. AIMDRC supplies them positionally as `(run_id, instruction_no, sample_id, sample_igsn)`. Instruction numbers are zero-based. A repeated station appears as a distinct instruction number.

AIMDRM owns runtime `sample.transform` for HELIX and the COORD result cache. Author physical coordinates in their declared frame; do not pre-transform them and still label them `sample`.

## Transform prerequisite

AIMDDS records `requires_initial_transform` when sample-frame points appear before any transform-producing COORD instruction. AIMDRM verifies each selected sample can satisfy that prerequisite when starting the run. A COORD photo-only instruction does **not** satisfy it.

| Sequence | Initial transform required? |
| --- | --- |
| MAXIMA in `sample_holder` | No |
| HELIX in `flyer_grid` | No; transform is optional output metadata |
| COORD `{}` → SPHINX in `sample` | No, provided COORD succeeds during the run |
| COORD `photo_only: true` → MAXIMA in `sample` | Yes |
| MAXIMA in `sample` → COORD `{}` | Yes for the first instruction |

Stored transforms are associated with sample identity, not proof that the physical sample has remained mounted in the same pose. See [coordinates](coordinates.md).

## Script storage and evolution

AIMDDS stores the file, its size, schema version, transform requirement and instruction line ranges. Those line ranges support UI highlighting; they are not the input dictionaries themselves. If reliable line ranges cannot be computed, the parser falls back to `(1, 1)` ranges. Script file contents are immutable via the update endpoint; changed experiment instructions need a new upload.

Version-1 records may remain visible for history and filtering. Convert legacy point fields, add explicit frames/units, and upload version 2 rather than changing only the stored version number.

## Source map

AIMDDS `apps/system/utils.py` (`validate_run_script`, `_validate_points`, `parse_run_script`), `serializers.py`; AIMDRM `apps/opcua/admin_client.py` and `coordinates.py`. [Controller inputs](../index.md#start-here).
