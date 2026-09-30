---
title: "Controller development interface"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 12 months
safety_level: informational
tags: [software, controls]
---

# Controller development interface

A station controller is an implementation of `apps.controller.interface.IController`, installed within AIMDRC. The shared factory injects an `IErrorService` and imports the class from `CONTROLLER_CLASS_PATH`.

## Required methods

| Async method | Contract |
| --- | --- |
| `open() -> None` | Make station access available for transfer; can be a no-op if no access hardware exists |
| `close() -> None` | Close station access before warmup/run and at completion |
| `get_status() -> dict` | Report controller-specific diagnostic status |
| `warmup(*args, **kwargs) -> dict` | Prepare for ingress; normal return permits ingress |
| `run(*args, **kwargs) -> dict` | Execute the instruction; normal return permits egress after optional result write |
| `cancel(*args, **kwargs) -> dict` | Attempt cancellation/cleanup within shared client's configured timeout |

`SyncControllerMixin` provides convenience wrappers outside an active event loop. Production lifecycle methods remain asynchronous.

## Input contract

AIMDRC calls warmup and run with positional `(run_id, instruction_no, sample_id, sample_igsn)` plus decoded `Input` kwargs. `parse_args()` enforces this shared identity boundary. Cancel receives identity but not the run kwargs from the status handler. Persist required cancellation context in controller state rather than relying on kwargs being replayed.

Physical points arrive as `sample.points` in holder millimeters. HELIX uses flyer-grid values. Controller-specific parsing should be separated from hardware calls; keep units, defaults, validation and diagnostics explicit.

## Return and failure semantics

A returned dictionary is successful completion to AIMDRC. Returning `{"status":"failed"}` still allows the next lifecycle step. Expected recoverable hardware conditions should remain in their recovery loop and report through the error service until recovery or cancellation. An exception escaping warmup/run is logged and prevents its next transition; it is not automatically converted into a universal failure/egress state.

`result` is reserved for JSON-serializable instruction output and is written before egress. In the current manager, only COORD gets an `Output/Result` node and coordinate persistence handling. Extend manager node creation and downstream persistence before introducing another result-producing controller.

The cancellation implementation has a narrower guarantee: AIMDRC ignores cancel dictionary status values, and after a cancellation timeout it reports an error then proceeds to `CNLD`. Design changes to cancellation as a shared protocol change, not just a new return string.

## Error pattern

```python
await wait_until_with_error(
  is_done=device_ready,
  timeout_s=timeout_s,
  error_service=self.error_service,
  error_code=DeviceErrors.NOT_READY,
  error_detail='Device has not confirmed readiness.',
)
```

Use an allocated code present in AIMDDS's canonical registry. The helper reports once after its timeout and clears the occurrence on recovery. It polls indefinitely with an error service; use an explicit outer timeout only when the intended failure behavior is defined. Preserve `CancelledError` and avoid blocking the asyncio loop with synchronous SDK calls; existing controllers use `asyncio.to_thread()` for those operations.

## Package conventions

Follow the supplied controllers: two-space Python indentation, triple-quoted module/class/method documentation, subsystem packages, constants and error enums next to the owning device adapter, typed result/settings objects where useful, and top-level controller orchestration. Keep duplicate metadata/output writing in a single result writer. Dependency files belong in `requirements/`; host integration belongs in `requirements/host/`.

## Adding a station

Update station identifiers/metadata in AIMDDS, AIMDRM and AIMDRC and the front-end station models as needed. Register its manager namespace and certificate, define script validation and coordinate semantics, allocate error definitions, install its controller and dependencies, and add meaningful mocked tests for device-state and cancellation behavior. A logical station mapped to an existing physical station needs deliberate robotics coordination.

Run unit tests without issuing hardware commands, check import/compilation in the target image, and commission device behavior through the appropriate instrument procedure. [Maintenance](maintenance.md) explains how to update references and examples.

## Source map

AIMDRC `apps/controller/interface.py`, `apps/opcua/client.py`, `apps/opcua/error_service.py`, `apps/utils.py`; supplied controller packages.
