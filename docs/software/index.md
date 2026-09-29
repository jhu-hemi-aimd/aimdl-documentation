---
title: "Software and controls"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 12 months
safety_level: informational
tags: [software, controls]
---

# Software and controls

The lab control stack turns a versioned JSON run script and a set of samples into station operations, robot transfers, and recorded experiment history. These pages document the supplied AIMD-L source snapshots. They are technical reference material pending owner review; use the instrument procedures for physical preparation and operation.

## Start here

| Goal | Read |
| --- | --- |
| Understand the system | [Architecture](architecture.md) |
| Use the application | [Operator guide](operator-guide.md) |
| Install services and station clients | [Setup](setup/index.md) |
| Author an experiment | [Run scripts](reference/run-scripts.md) and [examples](examples/index.md) |
| Understand station behavior | [MAXIMA](controllers/maxima.md), [HELIX](controllers/helix.md), [SPHINX](controllers/sphinx.md), [COORD](controllers/coord.md) |
| Integrate another application | [HTTP and WebSocket API](reference/api.md) |
| Inspect control communication | [OPC UA reference](reference/opcua.md) |
| Diagnose a failed operation | [Troubleshooting](operations/troubleshooting.md) and [error codes](reference/error-codes.md) and [symbol coverage](reference/error-symbols.md) |
| Extend a controller | [Controller interface](development/controller-interface.md) |
| Maintain this documentation | [Maintenance](development/maintenance.md) and [source snapshot](reference/source-snapshot.md) |

## Repository responsibilities

| Repository | Responsibility | Execution location |
| --- | --- | --- |
| [AIMDAS](repositories/aimdas.md) | Angular application, operator workflows, HTTP requests and live views | Web service and browser |
| [AIMDDS](repositories/aimdds.md) | Authentication, database records, script validation, API, WebSocket broadcasts | Central data service |
| [AIMDRM](repositories/aimdrm.md) | Scheduling, OPC UA server, robotics coordination, state and error forwarding | Central run manager |
| [AIMDRC](repositories/aimdrc.md) | Shared station state machine, controller lifecycle, OPC UA connection | One instance per station |
| `maxima`, `helix`, `sphinx`, `coord` | Device-specific behavior installed as `apps.controller` in AIMDRC | Associated station computer |

The supplied sources include station identifiers for `profile` and `engrave`, but do not include their controllers. Those names and reserved error ranges do not establish an implemented API or run-script contract.

## Scope

The [source review notes](reference/source-review.md) identify implementation limitations and differences from older README examples. All numbers in controller examples come from the supplied code or run script; they are examples, not a recommended experimental recipe. This work does not replace or amend the [lab safety documentation](../safety/index.md), MAXIMA procedures, or [HELIX laser safety plan](../instruments/helix/safety/safety.md).
