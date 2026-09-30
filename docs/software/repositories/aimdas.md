---
title: "AIMDAS application service"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 12 months
safety_level: informational
tags: [software, controls]
---

# AIMDAS application service

AIMDAS is the Angular/Angular Material front end. Apache serves the application; the browser calls AIMDDS for authentication and data, and subscribes to its WebSocket streams. It does not schedule instructions or implement hardware control.

## User-facing areas

The [operator guide](../operator-guide.md) describes each route and its actions. The core operational screens are Start run, System status, Run details and Run scripts. The remaining screens provide scheduling, sample history, media, account administration and documentation. The Reports page is a placeholder in this snapshot.

## Implementation map

| Location under `src/ng/src/app` | Purpose |
| --- | --- |
| `app-routing.module.ts` | Routes, browser tab titles and start-run dirty-form guard |
| `authentication/` | Sign-in route matching and authentication service |
| `rest.service.ts` | Shared HTTP request handling |
| `base/base.service.ts` | Appointments, media, profiles and samples |
| `system/system.service.ts` | Run, script and station requests; system/run WebSockets |
| `system/start-run/` | Script selection, sample slots and run submission |
| `system/system-status/` | Live run, conveyor, error, station and camera views |
| `system/run-details/` | Instruction progress, errors, script and notes |
| `system/_models/` | Typed run, station, error and physical-location data |
| `system/_components/` | Shared conveyor and status/error displays |
| `base/sample-details/` | Experimental data grouped by station or run |
| `documentation/` | Documentation integration |

`BufferSlot` includes processed state; `ConveyorSlot` includes HMI visibility; `StationState` includes enablement, robot-auto state, run-client health, assignment and status. These share sample identity rather than pretending every physical location has the same fields.

## Live updates

`SystemStateMessage` contains `active_runs`, `stations`, `buffers` and `conveyor`. Run-specific notifications provide a fresh serialized run detail. Appointment notifications trigger calendar updates. A working page and a working live connection are separate concerns: if a view stops updating, check AIMDDS/Daphne and the run manager status publisher as well as the browser.

`ADMIN` controls account administration; `SYS` controls lab operations and selected content mutations. Controls may be hidden or disabled in the UI, but AIMDDS enforces the server-side checks. See [API permissions](../reference/api.md).

## Development and deployment

Follow [service setup](../setup/services.md). The Angular project is `src/ng`; dependency versions and scripts are in its `package.json`. Run lint/build within the provisioned environment. The supplied source uses modern Angular template control flow and Material components. Keep TypeScript models synchronized with serialized backend and WebSocket payloads.

Camera streaming uses a separate go2rtc container, configured under `docker/local/go2rtc` or `docker/prod/go2rtc`. Streaming is a monitoring feature and is independent of experimental acquisition cameras in HELIX and COORD.

## Source map

`aimdas/README.md`, `src/ng/package.json`, the files above, and `src/ng/src/environments/`. [Source snapshot](../reference/source-snapshot.md).
