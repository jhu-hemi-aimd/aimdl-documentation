---
title: "Source review and current limitations"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 12 months
safety_level: informational
tags: [software, controls]
---

# Source review and current limitations

These findings describe the supplied snapshots. They are documentation findings, not fixes to the control software. Recheck the corresponding source before treating a limitation as resolved.

| Area | Current implementation | Documentation consequence |
| --- | --- | --- |
| Pause/resume | AIMDDS raises permission-denied “not yet supported”; manager methods are stubs | UI/routes are not evidence of implemented pause/resume |
| MAXIMA calibration | `warmup()` unconditionally returns before calibration logic | `calibrate=true` does not cause calibration in this snapshot |
| MAXIMA adaptive collection | `adaptive_ct` is parsed then discarded | Count time remains the configured fixed time |
| MAXIMA detector distance | Bounds are 0–20; helper substitutes default 0 outside bounds | README example 70 does not mean the controller will move to 70 |
| MAXIMA beam size | SDK settings include spot width/height; older SOP says metadata only | Confirm physical application on deployed Proto hardware; source proves request construction only |
| SPHINX batch options | `batch_location` and `is_batch_process` are not read | Full SMHM example retains them; minimal example omits them |
| SPHINX readiness order | Sample-presence check occurs before microscope motion | Older README run sequence is stale |
| Shared cancel handling | Return strings ignored; timeout also leads to cancel postprocessing | Software `CNLD` is not proof of stop, safe position or full cleanup |
| HELIX cancel | Stops scope/PDV and disconnects; skips normal package disassembly | Physical package recovery may remain |
| COORD calibration | `CALIBRATION=None` | Pipeline is uncalibrated in supplied defaults |
| COORD refusal | Saves diagnostics, reports 6700 and raises | No normal egress/result; no automatic reacquisition in this path |
| Transform persistence | Cache first, database post best effort | Live and durable state can diverge |
| Shared result contract | Manager allocates result node only for COORD | New result producers need manager integration |
| RunError list | Nested view lacks `run_pk` parameter and parent filtering | Do not rely on it as a working run-scoped list endpoint |
| Query documentation | `simple` advertised but not a generic reserved filter parameter | Use implemented filter helper behavior |
| Scheduling readiness | Queue creation does not check enabled/robot-auto/client-health flags | Treat health and PLC enablement separately from queue eligibility |
| Heating-laser errors | HELIX declares 1060/1061, absent from AIMDDS and supplied PDF | Symbols documented separately; no invented canonical severity/action |
| Station placeholders | `profile` and `engrave` identifiers exist, controllers not supplied | Do not infer controller options or device setup |

## Registry coverage

The supplied PDF and AIMDDS registry contain the same set of 170 numeric codes. The Markdown generator uses the registry as the metadata authority and expands the station-specific robotics definitions. The [symbol reference](error-symbols.md) additionally lists declared controller names, including the unregistered heating-laser codes.

AIMDDS `RunError.definition` uses direct registry lookup. An unregistered code is not safely handled merely by the model's `__str__` fallback text; register metadata before enabling a new emitted code. The current HELIX heating-laser connection is excluded from the active experiment path, and 1060/1061 are declarations without call-site use in the supplied adapter.

## Scope of verification

These pages are derived from source and static examples, not a connected-lab test. The setup guide identifies missing vendor/native installation details rather than inventing steps. All new pages remain `needs-review` with `last_reviewed: null` until a responsible maintainer reviews them. Existing safety procedures retain their own review status.

[Source snapshot](source-snapshot.md) records input archive hashes. The delivery validation report records which automated checks ran and any environment limitation on the strict MkDocs build.
