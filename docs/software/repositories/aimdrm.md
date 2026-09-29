---
title: "AIMDRM run manager"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 12 months
safety_level: informational
tags: [software, controls]
---

# AIMDRM run manager

AIMDRM coordinates multiple samples and station clients. Its HTTP layer validates requests from AIMDDS and sends commands through an administrative OPC UA client. The long-running OPC UA server owns the active scheduling tasks, sample queues and robotics client.

## Scheduling decisions

For each active run, the scheduler examines the sample's instruction index and `REST` state. The supplied scheduler does not gate queue creation on station enablement, robot-auto state or client connectivity; those states are monitored or handled at other control boundaries. It reads the physical station buffer and ingress priority list once for each target group.

* If the sample is already in the destination buffer, enqueue it with priority `(instruction_index, run_id, buffer_index)`.
* Otherwise, add it to the destination ingress priority list if it is not already present.
* An in-flight set prevents the same sample/instruction assignment from being queued repeatedly.
* One worker per logical station waits for station `REST`, resolves the instruction input, assigns identity and sets `WARM`.

This is sample-level pipelining: different samples may execute different instructions at different stations. The order within each sample follows the script. It is not a promise of synchronized execution across stations.

## Assignment and cancellation

A per-station assignment lock serializes the final assignment with cancellation's inspection of that station. The worker checks `_canceled_runs` while holding this lock. The separate in-flight lock protects duplicate-assignment bookkeeping; it does not replace the station claim lock.

Cancellation marks the run canceled for scheduling, stops its scheduler, filters queued assignments, clears its in-flight entries and inspects each distinct station. Ingress/egress tasks are canceled with the corresponding robotics handshake cleanup; a station executing controller work receives `CNLG`. The manager removes applicable priority-list entries and waits for involved stations to release the run before persisting `CNLD`.

A cancel request is not equivalent to an emergency stop, and a software `CNLD` status alone does not confirm a safe physical position. Read [current cancellation limitations](../reference/source-review.md).

## Robotics boundary

The robotics client maintains its own reconnect loop and uses station-scoped locks for shared PLC state. It owns buffer preload, ingress/egress priority lists, processed-state changes and transfer handshakes. Buffer preload detects occupied target slots rather than overwriting them. Preload failures report structured errors such as `buffer_occupied` (409), `invalid_buffer_mapping` (400), or `preload_failed` (500).

After station completion, the manager increments the sample's instruction index and sets the sample back to `REST`. Consecutive instructions for the same logical station reset its processed state to `PREPROCESSED`. Otherwise the sample joins transport priority lists as needed, including final routing to outfeed. Completion includes the outfeed condition, not just the last controller return.

## Coordinate processing

`SourceInput` retains uploaded values. `Input` is prepared for the selected sample immediately before dispatch. Physical points become sample-holder millimeters; HELIX retains flyer-grid values and receives an optional runtime transform. COORD results are validated and cached before the sample advances. Persistence to AIMDDS is best effort after caching, so a persistence error may leave live and durable transform state different.

## Health and errors

`RunClientMonitor` creates one disconnect occurrence for each affected station per run and clears it on reconnection. `ErrorMirror` forwards station error objects into AIMDDS records. The system status poller publishes the active run IDs, station state, buffers and conveyor. See [OPC UA](../reference/opcua.md) and [error handling](../operations/troubleshooting.md).

## Source map

`aimdrm/src/api/apps/opcua/server.py` (`_schedule_ready_samples`, `_run_assignment_queue_worker`, `cancel_run`, `_advance_sample`); `admin_client.py`; `robotics/client.py`; `run_client_monitor.py`; `error_mirror.py`. [Setup](../setup/services.md) · [source snapshot](../reference/source-snapshot.md).
