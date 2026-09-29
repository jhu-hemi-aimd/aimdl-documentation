---
title: "AIMDRC generalized run client"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 12 months
safety_level: informational
tags: [software, controls]
---

# AIMDRC generalized run client

AIMDRC provides the shared execution shell on each station computer. The installed controller implements device operations; the shared client handles the OPC UA session, station status subscription, heartbeat, input decoding, result publication and error reporting.

## State-driven controller calls

| Received state | Shared client behavior | Normal next state |
| --- | --- | --- |
| `REST` | No controller action | Assigned by manager |
| `WARM` | Read input; close access; call `warmup(run_id, instruction_no, sample_id, sample_igsn, **input)` | Open access, then `INGR` |
| `INGR` | Wait while AIMDRM performs ingress | Manager sets `PROG` |
| `PROG` | Read input; close access; call `run(...)` | Write reserved `result`, open access, then `EGRS` |
| `EGRS` | Wait while AIMDRM performs egress | Manager sets `CPLT` |
| `CPLT` | Close access | Manager resets station |
| `CNLG` | Cancel the active task; call `cancel(...)` with the configured timeout | Open access, then `CNLD` |
| `CNLD` | No further controller action | Run cleanup |

Repeated `WARM` or `PROG` notifications are ignored while an active task exists. Exceptions from warmup or run are logged and do not request ingress/egress. A returned dictionary is treated as successful completion; a key such as `status: failed` does not change that behavior.

## Connection and results

The client resolves the station namespace using the configured manager domain and station name. It uses certificate-based OPC UA security, reconnects after transport failures and recreates per-connection tasks. Input reads, heartbeat/status writes and result writes use reconnect-safe operations. Reconnection alone does not establish exactly-once execution of a device command or recover arbitrary hardware state.

Only the reserved `result` key is serialized into `Output/Result`. Other output fields, such as `data_directory`, are logged; they are not automatically uploaded or persisted as instruction-result records. In this AIMDRM snapshot, `Output/Result` is created for COORD instructions. Adding another result-producing controller requires extending that manager-side setup.

## Controller installation

Install the chosen controller under `src/api/apps/controller`, preserving the shared `interface.py`. The default factory path is `apps.controller.controller.Controller`. Set `NAME`, manager address, certificate and private-key paths in the selected settings module. The controller package is included before the Docker dependency-install steps, so dependency changes require rebuilding the image.

See [station setup](../setup/stations.md), [controller interface](../development/controller-interface.md) and [source review notes](../reference/source-review.md) for cancellation behavior and limitations.

## Source map

`aimdrc/src/api/apps/opcua/client.py`, `error_service.py`, `apps/controller/interface.py`, `apps/utils.py`, and `config/settings/`. [Source snapshot](../reference/source-snapshot.md).
