---
title: "COORD controller"
status: needs-review
owner_team: software-team
primary_contact: null
last_reviewed: null
review_cycle: 6 months
safety_level: operational
tags: [software, controls]
---

# COORD controller

COORD acquires an overhead image through Teledyne FLIR PySpin/Spinnaker, measures the sample relative to the holder, and returns a canonical transform through AIMDRC. `NAME='coord'` maps to physical station 6. The vision pipeline executes locally; AIMDRM handles caching and persistence.

## Run inputs

| Input | Default | Behavior |
| --- | --- | --- |
| Empty object `{}` | Transform mode | Acquire, detect, validate and publish a transform |
| `photo_only` | false | When true, save image/metadata without calculating a sample transform |

AIMDDS rejects other COORD input keys and non-Boolean `photo_only`. Direct controller calls also validate this flag, warning and defaulting an invalid value. Identity comes from AIMDRC positional arguments. Camera settings, fiducial geometry, calibration and thresholds live in controller constants rather than the run script.

## Components and API boundary

| Component | Responsibility |
| --- | --- |
| `top_camera/camera.py` | PySpin camera discovery, connection, configuration, acquisition, retries and disconnect |
| `experiment/settings.py` | Parse shared identity/flag and create the output directory |
| `detection/detector.py` | Holder/dot/tag measurement and diagnostic rendering |
| `detection/solve.py` | Pose solving and clean/degraded/refused confidence assessment |
| `controller.py::_build_transform()` | Construct finite canonical result and offset holder origin |
| `result_writer.py` | Save raw image, overlay, metadata and optional transform once |

Warmup/open/close are no-ops. Run connects the camera on demand, captures a grayscale image, dispatches OpenCV work through `asyncio.to_thread()`, saves artifacts and disconnects on normal/error completion. Cancellation owns its cleanup path.

## Transform mode

Accepted `clean` and `degraded` measurements produce the same canonical result shape. A refused measurement or invalid transform saves diagnostic files, reports code [6700](../reference/error-codes.md#error-6700), and raises instead of returning normally. AIMDRC logs the failed run task and does not request egress. The controller does not automatically reacquire after a refusal in this path; recovery requires the documented client restart or run cancellation after diagnosis.

```json
{
  "result": {
    "algorithm_version": "3.5.0",
    "matrix": [[1.0, 0.0], [0.0, 1.0]],
    "translation": [0.0, 0.0],
    "rms_error_mm": 0.1
  }
}
```

This is the supplied example result contract, not a measured transform. RMS is converted from pixel residual using the measured pixel scale. Translation subtracts the configured sample-window origin offset. AIMDRM adds the instruction-status ID only when posting to AIMDDS.

## Photo-only mode

Photo-only saves the raw image and an overlay. The overlay includes holder axes when holder detection succeeds; that detection is diagnostic and does not prevent saving the photo. Metadata records `mode: photo_only`, `transform: null` and holder diagnostics. The controller returns `photo_only`, elapsed time and data directory, but no `result`.

Photo-only neither creates a new transform nor invalidates an existing one. It does not count as a prerequisite for later sample-frame points. See [run scripts](../reference/run-scripts.md).

## Artifacts and calibration status

Output directory: `/opt/aimdrc/data/{igsn}_{sample_id}_{instruction_no}_{run_id}_{timestamp}/`.

| File | Transform accepted | Refused/invalid | Photo-only |
| --- | --- | --- | --- |
| `raw.png` | Yes | Yes | Yes |
| `overlay.png` | Yes | Yes | Yes |
| `metadata.json` | Yes | Yes | Yes |
| `transform.json` | Yes | No | No |

Metadata includes algorithm version, camera settings, identity, image shape/dtype, elapsed time, diagnostics and applied holder-origin offset. `CALIBRATION` is `None` in the supplied constants: the pipeline reports itself uncalibrated and derives scale from observed features. Complete bench calibration and review thresholds before treating output as a validated metrology result.

## Examples

[Download coord.json](../examples/coord.json).

```json
{
  "schema_version": 2,
  "instructions": [
    [
      "coord",
      {}
    ]
  ]
}
```

[Download coord-photo-only.json](../examples/coord-photo-only.json).

```json
{
  "schema_version": 2,
  "instructions": [
    [
      "coord",
      {
        "photo_only": true
      }
    ]
  ]
}
```

## Setup and source map

[Station setup](../setup/stations.md#coord) describes the CPython 3.12 SDK requirement and Windows/WSL camera attachment. Files: `controller.py`, `experiment/`, `top_camera/`, `detection/`, `result_writer.py`, `requirements/deps/README.md`. [Errors: 6500–6999](../reference/error-codes.md).
