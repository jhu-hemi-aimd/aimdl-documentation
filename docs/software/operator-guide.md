---
title: "Application operator guide"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 6 months
safety_level: operational
tags: [software, controls]
---

# Application operator guide

Use AIMDAS to prepare and monitor runs through AIMDDS. The actions below describe the supplied application; device preparation remains governed by the instrument procedures.

## Screens and actions

| Route | Available actions and information |
| --- | --- |
| `/` | Navigate to lab tools and content |
| `/calendar` | View appointments, filter by equipment, create bookings, edit/delete owned bookings, add comments, delete owned comments, export appointments |
| `/samples` | Search IGSNs and open sample details |
| `/samples/:id` | Browse experiment data grouped by station or run; open associated run/script/data links |
| `/runs/new` | Select or upload a script; choose infeed and outfeed; assign samples to buffer slots; clear selections; submit run |
| `/system` | Inspect current runs and per-sample progress, conveyor/buffers, active errors, station state and cameras; select a run for focused inspection |
| `/runs` | Filter and inspect historical runs |
| `/runs/:id` | Inspect instruction progress, errors, script and notes; add/edit/delete authorized notes; cancel or clear when allowed |
| `/run-scripts` | Upload/create, preview, download, rename/edit metadata, copy and delete scripts; filter/sort including schema version |
| `/media` | Browse/download media; authorized users can upload and edit/delete owned content |
| `/users` | Administrators create and update profiles and roles |
| `/docs` | Open documentation |
| `/reports` | “Coming soon” placeholder |

`SYS` is the system role; `ADMIN` is the account-administration role. Calendar/comment edits are ownership-limited. Media edits additionally require `SYS`; run-note edits require `SYS` and ownership. Script mutations require `SYS`. API enforcement is the authoritative permission boundary.

## Prepare a run in the application

1. Upload a [schema-version-2 script](reference/run-scripts.md), or choose an existing one. A schema-version-1 historical record cannot start a new run.
2. Select the physical infeed and outfeed station numbers. Match sample selections to the actual buffer layout. Slot keys sent to AIMDDS are zero-based, 0–47.
3. Select each sample once. Samples in another nonterminal run are rejected. If the script uses sample-frame coordinates before a transform-producing COORD instruction, each sample needs a stored transform.
4. Submit the run. Read any returned validation or buffer-occupancy error before retrying.
5. Monitor System status and Run details. Compare instruction state, station identity, client health, physical location and active errors rather than relying on only the run's top-level status.

The dirty-form guard protects an unfinished start-run form from accidental navigation. A submitted run continues on the services after the browser closes.

## Lifecycle actions

| Action | Actual behavior |
| --- | --- |
| Cancel | Requests controller/task cancellation and manager cleanup; does not constitute a hardware emergency stop |
| Clear | Allowed for `CPLT` or `CNLD`; removes the run from live manager state, not database history |
| Pause/resume | Routes and UI code exist, but AIMDDS rejects both as “not yet supported”; AIMDRM implementations are stubs |
| Station enabled / robot auto | Patches a physical station's PLC settings; changes are commands, and HTTP success is not completion feedback |
| Restart server | AIMDDS rejects restart while any database run is nonterminal; restarting rebuilds volatile server state |

The error table shows occurrence details and canonical recommended actions. There is no ordinary-browser error-acknowledgment API in the supplied source; error mutation endpoints use service authentication. An inactive error is historical, while an acknowledged error can still be active.

## Source map

AIMDAS route components and shared services under `src/ng/src/app`; AIMDDS `apps/base/views.py` and `apps/system/views.py`. [API reference](reference/api.md) · [troubleshooting](operations/troubleshooting.md).
