---
title: "Data and recovery boundaries"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 6 months
safety_level: operational
tags: [software, controls]
---

# Data and recovery boundaries

The database, manager address space and instruments preserve different information. A reliable recovery starts by identifying which state remains available.

## Data locations

| Data | Owner / location |
| --- | --- |
| Profiles, run metadata, instruction statuses, errors, notes and coordinate history | AIMDDS database |
| Uploaded scripts/media | AIMDDS managed file storage under its configured data paths; persist `/opt/aimdds/data` |
| Active run/sample/station nodes and queues | AIMDRM process/OPC UA address space |
| MAXIMA raw and cleaned acquisition files | Shared detector data mounted at `/opt/aimdrc/data`, with automatic/manual subfolders |
| HELIX image captures and result CSV | Controller data directory; waveform files separately on scope `SAVE_DIR` |
| SPHINX measurements | InView-managed project/output location on the instrument host |
| COORD image, overlay, metadata and transform | Persistent controller data directory |
| Data-portal experiment links | External portal queried by AIMDDS sample detail logic |

Controller return dictionaries are not a generic file-transfer mechanism. AIMDRC logs ordinary fields, and only the reserved `result` value is written to the configured result node. COORD's canonical transform has a persistence path; arbitrary controller files do not automatically gain one.

## Restart implications

AIMDRM's server creates its address space on startup. The supplied code does not reconstruct a complete running experiment from the database after a manager restart. A reconnecting station client can resume communicating, but hardware commands already issued may have taken effect. Do not equate a new process with an empty device or cleared sample buffer.

The AIMDDS restart endpoint refuses while database runs are nonterminal. Shell restart scripts can still restart processes; use them as maintenance operations with knowledge of current hardware state. Preserve logs and reconcile station/PLC state before beginning another run.

## Clear versus cancel

Cancel requests termination of active work. Clear is available only after `CPLT` or `CNLD` and removes the run's live manager state. Neither operation is a data-erasure API for historical runs. Clearing error displays or acknowledging an occurrence also does not reverse a hardware fault.

## Coordinate persistence

AIMDRM caches a validated COORD result before attempting the AIMDDS post. That post is best effort. The current run may use the cached transform even when later runs cannot retrieve it. The newest stored transform is selected by sample ID; a changed mounting can invalidate its physical applicability without changing the sample ID.

## Backup scope

Preserve the database together with uploaded script/media storage and instrument data. Also retain source revisions, dependency/vendor versions, calibration/configuration files and deployment configuration through the appropriate protected backup process. A source zip without the database and instrument files is not a lab-data backup. Never add private keys, service tokens or share passwords to a documentation archive.

## Source map

AIMDDS `apps/system/models.py`, `apps/base/models.py`; AIMDRM `opcua/server.py` startup/clear/result handling; controller result writers and READMEs. [Troubleshooting](troubleshooting.md).
